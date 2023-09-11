#Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Short Co-Rotating Dipole Animation

epsilon_0 = 8.854 * 10**-12 # PERMITIVITY OF FREE SPACE
d = np.linspace(-1,1,50)

X,Y = np.meshgrid(d,d)

mag = lambda R: np.sqrt(np.einsum('ijk,ijk->ij',R,R))
r = lambda X,Y,pc: np.array([X - pc[0], Y - pc[1]]).T
E = lambda R,q: q / 4 / np.pi / epsilon_0 * np.einsum('ijk,ij->ijk',R,1/mag(R)**3)

def EFC(X,Y,pca,pcb):
	return (E(r(X,Y,pca),pca[2])+E(r(X,Y,pcb),pcb[2])).T

fig, ax = plt.subplots()

#Instantiate Stream Object
stream = ax.streamplot(X,Y,X,Y)

#Main Update Function
#Note: Unfortunately the StreamPlotSet object does not have a set data method so the entire axis must be cleared
# and replotted with new data, this results in very poor performance for the animation
def update(i):
	ax.clear()
	ax.set_title("Co-Rotating Dipole EF")
	pca = np.array([.5*np.cos(2*np.pi*i/20),.5*np.sin(2*np.pi*i/20),-1])
	pcb = np.array([-.5*np.cos(2*np.pi*i/20),-.5*np.sin(2*np.pi*i/20),1])
	stream = ax.streamplot(X,Y,*EFC(X,Y,pca,pcb),arrowsize=0)
	plt.plot(*pca[:-1],"ro",c="r")
	plt.plot(*pcb[:-1],"ro",c="b")
	return stream

#Instantiate Animation Object
ani = FuncAnimation(fig,update,interval=.1,frames=1000)

#plot :3
plt.show()
quit()