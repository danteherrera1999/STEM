import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from random import randint

"""
This is a Brownian motion simulation. It demonstrates how smaller particles can cause a larger particle to exhibit random motion. This 
simulation is an inherently macro scale animation but smaller particles may be invisible to the human eye making the random motion of
small particles that we can see seem spontaneous and strange. Adjust the "visible" parameter to view/hide the small particles.
"""
visible = True

class particle:
	# Initialize the particle with an initial position and velocity
	def __init__(self,x,y,r,Vx,Vy,mass=1,color='b',alpha = int(visible)):
		self.position = np.array((x,y)).astype(float)
		self.radius = r
		self.velocity = np.array((Vx,Vy)).astype(float)
		self.color = color
		self.cooldown = 0
		self.mass = mass
		self.collision_history = {}
		self.alpha = alpha
	# Generate the circle patch
	def plot(self,ax):
		self.patch = plt.Circle(self.position,self.radius,color=self.color,fill=False,alpha = self.alpha)
		return self.patch
	# Bounce a particle back if it hits the plot boundary
	def check_boundary(self):	
		if self.cooldown == 0:
			if abs(50-self.position[0]) > 50-self.radius: self.velocity[0] *= -1
			if abs(50-self.position[1]) > 50-self.radius: self.velocity[1] *= -1
			self.cooldown = 1
	# Advance the particle's position in time
	def step_position(self,dt):
		self.check_boundary()
		self.position += self.velocity * dt
		self.patch.center = self.position
		if self.cooldown >0: self.cooldown -= 1
		for collision in list(self.collision_history.keys()):
			if self.collision_history[collision]==0: del self.collision_history[collision]
			else: self.collision_history[collision] -= 1
		return self.patch
	# Update the recent collision dictionary
	def add_collision(self,collision):
		# This will prevent a particle from colliding with another ball for the number of iterations below
		if not collision in self.collision_history.keys(): self.collision_history[collision] = 10 

# Generate the smaller particles
def generate_ordered_particles(N,upper_bound,right_bound,radius):
	n = int(np.sqrt(N))
	vmag = 30 # Sets velocity maximum for each axis
	items = [particle(x,y,radius,randint(-vmag,vmag)/10,randint(-vmag,vmag)/10) for x in np.linspace(radius*2,right_bound-2*radius,n) for y in np.linspace(2*radius,upper_bound-2*radius,n)]
	return np.array(items).tolist(),n**2

# Calculates the space between particles
distance = lambda a,b: np.sqrt((b[1]-a[1])**2+(b[0]-a[0])**2) - (b[2]+a[2])

# This function calculates the distance between all pairs of particles and returns the indices of colliding particles
def get_collisions(particles,N):
	collisions = []
	particles = np.array([(*particle.position,particle.radius) for particle in particles])
	for i in range(1,len(particles)):
		cs = np.argwhere(distance(particles.T,np.roll(particles,i,axis=0).T)<=0)
		for c in cs:
			collisions.append(np.sort([c[0],(c[0]-i)%N]))
	return np.unique(collisions,axis=0)

N = 144 # This number will be coerced to the nearest square

particles,N = generate_ordered_particles(N,100,100,1)

# This adds the large particle
particles=  np.array(particles+[particle(50,50,5,0,0,mass=5,color='r',alpha=1)])
N += 1

# Instantiate the plot
fig,ax = plt.subplots()
ax.set_ylim(0,100)
ax.set_xlim(0,100)
ax.set_aspect(1)

# Creates a patch collection for efficient animation
particle_patches = PatchCollection([particles[i].plot(ax) for i in range(len(particles))],match_original=True)
ax.add_collection(particle_patches)

# This is the main update loop for the animation
def update(z):
	collisions = get_collisions(particles,N) # Calculate collisions
	for (i,j) in collisions:
		if not (i,j) in particles[i].collision_history.keys(): # Particles keep a temporary dictionary of recent collisions to reduce jitter
			v1,v2,m1,m2 = particles[i].velocity,particles[j].velocity,particles[i].mass,particles[j].mass
			# Calculate elastic collision final velocities
			M = m1+m2
			particles[i].velocity = ((m1-m2)/M)*v1+(2*m2/M)*v2
			particles[j].velocity = (2*m1/M)*v1+((m2-m1)/M)*v2
			# Add this particle pair collision to the particle's recent collisions dictionary
			particles[i].add_collision((i,j))
			particles[j].add_collision((i,j))
	particle_patches.set_paths([particle.step_position(.1) for particle in particles])
	return particle_patches,

# Instantiate and show the animation
ani = FuncAnimation(fig,update,interval=.1,frames=1000,blit=True)
plt.show()




