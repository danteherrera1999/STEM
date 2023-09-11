#Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Simple Lissajous Curve animator, feel free to change parameters, main idea is that the output is very sensitive to initial conditons
#Current parameters match figure 3-3 (pg. 106) from "Classical Dynamics of Particles And Systems" from Stephen Thornton and Jerry Marion

#Lissajous Curve Parameters
A  = 1
B = 1
w_0 = 1/2
w_1 = 3/4 * w_0
alpha = np.pi/2
delta = 0
N=1000 #number of points

#Instantiate Plot Object
fig, ax = plt.subplots()
ax.set_ylim(-B,B)
ax.set_xlim(-A,A)
ax.set_aspect(1)

#Set Domain
t=np.linspace(0,100,N)

#Curve functions
x = lambda t: A * np.cos(w_0*t - alpha)
y = lambda t: B * np.cos(w_1*t - (alpha - delta))

#instantiate data
xs,ys = x(t), y(t)
ln, = ax.plot([],[])

#Main Update Function
def update(frame):
	ln.set_data([xs[:frame],ys[:frame]])
	return ln

#Instantiate Animation Object
ani = FuncAnimation(fig,update,interval=.1,frames=N)

#plot :3
plt.show()
