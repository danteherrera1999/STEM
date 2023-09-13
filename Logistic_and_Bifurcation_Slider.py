#module imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# This demo shows how the logistic population growth and it's bifurcation diagram evolve as functions of 
# alpha and the initial population

#logistic equation
f = lambda alpha, x: alpha * x * ( 1 - x)
d = np.linspace(0,1,1000)
fig, ax = plt.subplots(2)
line = [ax[1].plot(d,f(2,d))[0],ax[1].plot([],[],ls='--',color='red',label='Population Evolution')[0],ax[0].plot([],[],'ro',color='k')[0],ax[0].plot([],[],'ro')[0]]
ax[1].set_ylabel(r'$x_{n+1}$',fontsize=20)
ax[1].set_xlabel(r'$x_{n}$',fontsize=20)
ax[1].set_aspect(1)
ax[0].set_xlim(2,4)
ax[0].set_ylim(0,1)
tol = .001
i_max = 100

aspace = np.linspace(2,4,100)
def gen_bif_plot(x_0):
	bif_data = []	
	for alph in aspace:
		x = x_0
		for i in range(50):
			x = f(alph,x)
		for i in range(50):
			bif_data.append([alph,x])
			x = f(alph,x)
	line[2].set_data(np.array(bif_data).T)	

gen_bif_plot(.5)

def update(val):
	global line
	i=0
	x = x_0_slider.val
	a = alpha_slider.val
	xs,ys = [x],[0]
	line[0].set_data(d,f(a,d))
	pop_max = np.max(line[0].get_data()[1])
	ax[1].set_ylim(0,pop_max+.1)
	while i <= i_max:
		x_next = f(a,x)
		xs += [x,x_next]
		ys += [x_next,x_next]
		x = x_next
		i += 1
	xs.append(x)
	ys.append(f(a,x))
	l = int(len(xs)/2)
	line[3].set_data(np.repeat(a,l),xs[l:])
	line[1].set_data(xs,ys)	


alpha_axis = fig.add_axes([.95,.1,.03,.7])
alpha_slider = Slider(ax=alpha_axis,label=r'$x_{0}$',valmin=2,valmax=4,valinit=2,orientation='vertical')
alpha_slider.on_changed(update)

x_0_axis = fig.add_axes([.16,.1,.705,.03])
x_0_slider = Slider(ax=x_0_axis,label=r'$x_{0}$',valmin=.0001,valmax=.9999,valinit=.5)
x_0_slider.on_changed(update)
x_0_slider.on_changed(gen_bif_plot)
update(1)

plt.show()














