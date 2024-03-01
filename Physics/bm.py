import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from random import randint
import timeit


reflect = lambda V1,V2: V1 - 2 * V1 * V2
class particle:
	def __init__(self,x,y,r,Vx,Vy,mass=1,color='b'):
		self.position = np.array((x,y)).astype(float)
		self.radius = r
		self.velocity = np.array((Vx,Vy)).astype(float)
		self.color = color
		self.cooldown = 0
		self.mass = mass
		self.collision_history = {}
	def plot(self,ax):
		self.patch = plt.Circle(self.position,self.radius,color=self.color,fill=False)
		return self.patch
	def check_boundary(self):	
		if self.cooldown == 0:
			if abs(50-self.position[0]) > 50-self.radius: self.velocity[0] = -self.velocity[0]
			if abs(50-self.position[1]) > 50-self.radius: self.velocity[1] = -self.velocity[1]
			self.cooldown = 10
	def step_position(self,dt):
		self.check_boundary()
		self.position += self.velocity * dt
		self.patch.center = self.position
		if self.cooldown >0: self.cooldown -= 1
		for collision in list(self.collision_history.keys()):
			if self.collision_history[collision]==1: del self.collision_history[collision]
			else: self.collision_history[collision] -= 1
		return self.patch
	def add_collision(self,collision):
		if not collision in self.collision_history.keys(): self.collision_history[collision] = 30

def generate_random_particles(N,upper_bound,right_bound,max_radius,min_radius=0):
	items = []
	for i in range(N):
		radius = randint(min_radius if min_radius != 0 else max_radius,max_radius)
		x = randint(radius,right_bound-radius)
		y = randint(radius,upper_bound-radius)
		items.append(particle(x,y,radius,randint(-10,10)/10,randint(-10,10)/10))
	return np.array(items)

def generate_ordered_particles(N,upper_bound,right_bound,radius):
	n = int(np.sqrt(N))
	vmag = 20
	items = [particle(x,y,radius,randint(-vmag,vmag)/10,randint(-vmag,vmag)/10) for x in np.linspace(radius*2,right_bound-2*radius,n) for y in np.linspace(2*radius,upper_bound-2*radius,n)]
	return np.array(items)

distance = lambda a,b: np.sqrt((b[1]-a[1])**2+(b[0]-a[0])**2) - (b[2]+a[2])

def get_collisions(particles,N):
	collisions = []
	particles = np.array([(*particle.position,particle.radius) for particle in particles])
	for i in range(1,len(particles)):
		cs = np.argwhere(distance(particles.T,np.roll(particles,i,axis=0).T)<=0)
		for c in cs:
			collisions.append(np.sort([c[0],(c[0]-i)%N]))
	return np.unique(collisions,axis=0)

N = 100

particles = generate_ordered_particles(N,100,100,1).tolist()

particles=  np.array(particles+[particle(50,50,5,0,0,mass=5,color='r')])
collisions = get_collisions(particles,N)
cflat = np.array(collisions).flatten()
fig,ax = plt.subplots()
ax.set_ylim(0,100)
ax.set_xlim(0,100)
ax.set_aspect(1)

particle_patches = PatchCollection([particles[i].plot(ax) for i in range(len(particles))],match_original=True)
ax.add_collection(particle_patches)

def update(z):
	collisions = get_collisions(particles,N)
	for (i,j) in collisions:
		if not (i,j) in particles[i].collision_history.keys():
			v1,v2,m1,m2 = particles[i].velocity,particles[j].velocity,particles[i].mass,particles[j].mass
			M = m1+m2
			particles[i].velocity = ((m1-m2)/M)*v1+(2*m2/M)*v2
			particles[j].velocity = (2*m1/M)*v1+((m2-m1)/M)*v2
			particles[i].add_collision((i,j))
			particles[j].add_collision((i,j))
	particle_patches.set_paths([particle.step_position(.1) for particle in particles])
	return particle_patches,

ani = FuncAnimation(fig,update,interval=1,frames=10000,blit=True)

plt.show()




