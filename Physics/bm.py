import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randint
import timeit

def generate_random_objects(N,upper_bound,right_bound,min_radius,max_radius):
	items = []
	for i in range(N):
		radius = randint(min_radius,max_radius)
		x = randint(radius,right_bound-radius)
		y = randint(radius,upper_bound-radius)
		items.append((x,y,radius))
	return np.array(items)

def generate_ordered_objects(N,upper_bound,right_bound,radius):
	n = int(np.sqrt(N))
	items = [(x,y,radius) for x in np.linspace(radius*2,right_bound-2*radius,n) for y in np.linspace(2*radius,upper_bound-2*radius,n)]
	return np.array(items)

distance = lambda a,b: np.sqrt((b[1]-a[1])**2+(b[0]-a[0])**2) - (b[2]+a[2])

def get_collisions(items):
	collisions = []
	for i in range(len(items)-1):
		for j in range(i+1,len(items)):
			if distance(items[j],items[i])<=0:
				collisions.append((i,j))
	return collisions

def get_collisions_2(items,N):
	collisions = []
	for i in range(1,len(items)):
		cs = np.argwhere(distance(items.T,np.roll(items,i,axis=0).T)<=0)
		for c in cs:
			collisions.append(np.sort([c[0],(c[0]-i)%N]))
	return np.unique(collisions,axis=0)

N = 100

items = generate_ordered_objects(N,100,100,1)

collisions = get_collisions_2(items,N)
cflat = np.array(collisions).flatten()
fig,ax = plt.subplots()
ax.set_ylim(0,100)
ax.set_xlim(0,100)
ax.set_aspect(1)
for i in range(len(items)):
	(x,y,r) = items[i]
	color = 'r' if i in cflat else 'b'
	cir = plt.Circle((x,y),r,color=color,fill=False)
	ax.add_patch(cir)
plt.show()




