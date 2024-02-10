import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Simple ray tracing animation for parabolic mirror


#Mirror parameters
f = 4
A = 1 / 4 / f
fp = np.array([0,f])
ref = lambda v,s: 2 * s * np.dot(v,s) - v
u = lambda v: v / np.sqrt(np.dot(v,v))
der = lambda x: u(np.array([1,2*A*x]))
para = lambda x: A * x ** 2

L0 = 2
n = 25 #Number of lines


d = np.linspace(-1,1,1000)
fig, ax = plt.subplots()
fd = np.linspace(-1,1,n)
thetas = np.linspace(-30,30,300) * np.pi/ 180
thetas = np.concatenate((thetas,thetas[::-1]))
lines = [ax.plot(d,para(d),c='k')[0]]
ax.set_aspect('equal') 
v = np.array([np.sin(thetas[0]),-np.cos(thetas[0])])
LCs = []
for i in fd:
	p0 = np.array([i,para(i)])
	LC = np.sqrt(np.dot(fp-p0,fp-p0))
	LCs.append(LC)
	vr = u(ref(v,der(i))) * LC + p0
	vo = p0 - v * LC
	lines.append(ax.plot([p0[0],vr[0]],[p0[1],vr[1]],c='r',ls='--')[0])
	lines.append(ax.plot([p0[0],vo[0]],[p0[1],vo[1]],c='y',ls='--')[0])

plt.xlim(-2,2)
plt.title('Ray Tracing Simulation for Parabolic Mirror with f = 4')
def update(i):
	v = np.array([np.sin(thetas[int(i)]),-np.cos(thetas[int(i)])])
	for z in range(len(fd)):
		x = fd[z]
		p0 = np.array([x,para(x)])	
		vr = u(ref(v,der(x))) * LCs[z] + p0
		vo = p0 - v * L0
		lines[2*z+1].set_data([p0[0],vr[0]],[p0[1],vr[1]])
		lines[2*z+2].set_data([p0[0],vo[0]],[p0[1],vo[1]])
	return lines


ani = FuncAnimation(fig,update,interval=1/2,frames=600,blit='True')

#plot :3
plt.show()
