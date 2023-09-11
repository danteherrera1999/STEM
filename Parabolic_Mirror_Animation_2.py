import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#THIS IS A MIRROR REFERENCE FRAME CALCULATION


Fs = np.linspace(-1,1,100)
Fs = np.concatenate((Fs,Fs[::-1]))
A = lambda f: 1 / 4 / f
ref = lambda v,s: 2 * s * np.dot(v,s) - v
u = lambda v: v / np.sqrt(np.dot(v,v))
der = lambda x, a: u(np.array([1,2*a*x]))
para = lambda x, a: a * x ** 2

L0 = 2
n = 25

d = np.linspace(-1,1,1000)

fig, ax = plt.subplots()
fd = np.linspace(-1,1,n)
lines = [ax.plot(d,para(d,A(Fs[0])),c='k')[0]]
#ax.set_aspect('equal') 
v = np.array([0,-1])

for i in fd:
	fp = np.array([0,Fs[0]])
	a = A(fp[-1])
	p0 = np.array([i,para(i,a)])
	LC = np.sqrt(np.dot(fp-p0,fp-p0))
	vr = u(ref(v,der(i,a))) * LC + p0
	lines.append(ax.plot([p0[0],vr[0]],[p0[1],vr[1]],c='r',ls='--')[0])
lines.append(ax.plot(*fp,'ro',c='k')[0])

def update(i):
	fp = np.array([0,Fs[i]])
	a = A(fp[-1])
	lines[0].set_data(d,para(d,A(Fs[i])))
	lines[-1].set_data(fp)
	for z in range(len(fd)):
		x = fd[z]
		f = fp[-1]
		p0 = np.array([x,para(x,a)])	
		vr = f / abs(f) * u(ref(v,der(x,a))) * np.sqrt(np.dot(fp-p0,fp-p0)) + p0
		lines[z+1].set_data([p0[0],vr[0]],[p0[1],vr[1]])
	return lines


ani = FuncAnimation(fig,update,interval=5,frames=200,blit='True')
plt.show()