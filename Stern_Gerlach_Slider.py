#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# short and sweet script to show Stern Gerlach interferometer output as a function of the input state
# alpha^2 represents the intensity of the up state beam, the intensity of the down state beam is defined as 1-alpha^2
# when alpha^2 is 0, only the down state beam is present, and the output beam is split equally, the same output occurs
# when alpha^2 is 1; however, when the output state is .5 (that is, the down and up state beams are of equal intensity),
# the output beam is 100% up. This could represent beam intensity, or particle state probability, etc. either way the important
# take away is that the interference creats the somewhat counter-intuitive output

comp = lambda x: np.sqrt(1-x**2)
BS1 = np.array([[1,1],[1,-1]]) * 1/np.sqrt(2)
BS1_OUT = lambda vec: np.matmul(BS1,np.array(vec))
fig, ax = plt.subplots()
ax.set_xlim(0,2)
ax.set_ylim(0,2)
Rays = []
Rays.append(ax.plot([0,1],[2,1],color='red',alpha=1))
Rays.append(ax.plot([0,1],[0,1],color='red',alpha=0))
Rays.append(ax.plot([1,2],[1,2],color='red',alpha=BS1_OUT([1,0])[0]))
Rays.append(ax.plot([1,2],[1,0],color='red',alpha=BS1_OUT([1,0])[1]))

ax_alpha = fig.add_axes([.1,.1,.8,.1])
alpha_slider = Slider(ax=ax_alpha,label=r"$\alpha^2$",valmin=0,valmax=1,valinit=1)
def update(val):
	alpha = np.sqrt(alpha_slider.val)
	beta = np.sqrt(1-alpha**2)
	bs1o = BS1_OUT([alpha,beta])
	plt.setp(Rays[0][0],alpha=alpha**2)
	plt.setp(Rays[1][0],alpha=beta**2)
	plt.setp(Rays[2][0],alpha=bs1o[0]**2)
	plt.setp(Rays[3][0],alpha=bs1o[1]**2)
alpha_slider.on_changed(update)	


plt.show()