#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#This is a small ray tracing simulation for a flat mirror with adjustable focal length, source position, and mirror angle



# Instantiate constants
W = 1 #Source Width
H = 2 #Source Height
F = 5 #Default Focal Length
N = 20 #Number of rays


fig, ax = plt.subplots()
d_mirror = np.array([-1,1])

#axes and sliders
axT = fig.add_axes([.2,.1,.6,.05])
T_slider = Slider(ax=axT,label=r"$\theta$",valmin=-90,valmax=90,valinit=0)
axH = fig.add_axes([.2,.05,.6,.05])
H_slider = Slider(ax=axH,label=r"$H$",valmin=1,valmax=10,valinit=2)
axF = fig.add_axes([.2,0,.6,.05])
F_slider = Slider(ax=axF,label=r"$F$",valmin=2,valmax=10,valinit=5)

#meat and potatos
def generate_plot(H,F,theta):
	ax.set_ylim(-5,5)
	ax.set_xlim(-5,5)
	theta *= np.pi / 180
	slope_mirror = -np.tan(theta)
	y_mirror = d_mirror * slope_mirror
	n_hat = np.array([-slope_mirror,1])
	n_hat = n_hat / (np.sqrt(np.dot(n_hat,n_hat)))
	ax.set_aspect(1)
	tx,ty=[np.cos(-theta),np.sin(-theta)]
	ax.plot([-tx,tx],[-ty,ty])
	#plot source
	XS = np.linspace(-W/2,W/2,N)
	for X in XS: #For each ray keep components perpendicular to the mirror and reflect parallel components
		slope = (-F)/(-X)
		Ix = (H-slope*X)/(slope_mirror-slope)
		Iy = slope_mirror*Ix
		ax.plot([X,Ix],[H,Iy],color='red')
		V = np.array([-Ix,Iy-F+H])
		V -= (2 * np.dot(V,n_hat) * n_hat)
		ax.plot([Ix,Ix+V[0]],[Iy,Iy+V[1]],color='red',ls='--')

#Update Function
def update(val):
	ax.clear()
	generate_plot(H_slider.val,F_slider.val,T_slider.val)

#Add slider event listeners
T_slider.on_changed(update)
H_slider.on_changed(update)
F_slider.on_changed(update)

#plot :3
generate_plot(2,5,0)
plt.show()
