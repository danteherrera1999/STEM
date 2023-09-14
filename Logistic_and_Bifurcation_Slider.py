#module imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# This demo shows how the logistic population growth and it's bifurcation diagram evolve as functions of 
# alpha and the initial population
# This demo is my solution to the example from section 4.7 "Mapping" of "Classical Dynamics of Particles and Systems"

#logistic equation
f = lambda alpha, x: alpha * x * ( 1 - x)
d = np.linspace(0,1,1000)

# Setting up plot objects to be updated later
fig, ax = plt.subplots(2)
line = [ax[1].plot(d,f(2,d))[0],ax[1].plot([],[],ls='--',color='red',label='Population Evolution')[0],ax[0].plot([],[],'ro')[0]]
ax[1].set_ylabel(r'$x_{n+1}$',fontsize=20)
ax[1].set_xlabel(r'$x_{n}$',fontsize=20)
ax[0].set_xlim(2,4)
ax[0].set_ylim(0,1)

#Number of bifurcation plot lines, i initially used round objects but it looked bad so I am instead building N curves
N= 100
streaks = [ax[0].plot([],[],color='k')[0] for i in range(N)]

#alpha values
aspace = np.linspace(2,4,200)

# Function to generate bifurcation plot
def gen_bif_plot(x_0):
	bif_data = []
	#For every alpha value
	for alph in aspace:
		#Generate list of 500 x values starting from initial x_0 and running through logistic iteration formula
		x = x_0
		xs = []
		for i in range(500):
			xs.append(x)			
			x = f(alph,x)
		#Only keep last N values (trying to ignore noise from early iterations), also sort them to keep lines neat
		bif_data.append(np.sort(np.array(xs)[-N:]))
	#Transpose bifurcation data and plot against alpha values	
	bif_data = np.array(bif_data).T
	for i in range(N):
		streaks[i].set_data(aspace,bif_data[i])

#Initialize bifurcation plot from x_0 = .5
gen_bif_plot(.5)

def update(val):
	x = x_0_slider.val
	a = alpha_slider.val
	xs = []
	line[0].set_data(d,f(a,d)) #Plot new logistic curve
	pop_max = np.max(line[0].get_data()[1]) #Resize plot to fit data
	ax[1].set_ylim(0,pop_max+.1)
	#Generate evolution from x_0
	for i in range(100):
		xs += [x,x]
		x = f(a,x)
	#Derive y values from x values
	ys = np.roll(xs,-1)
	ys[0],ys[-1]= 0,f(a,x)
	#Plot last N elements of x array on bifurcation plot
	line[2].set_data(np.repeat(a,N),xs[-N:])
	#Plot Evolution curve
	line[1].set_data(xs,ys)	

#Instantiate alpha slider and add event listener
alpha_axis = fig.add_axes([.95,.1,.03,.7])
alpha_slider = Slider(ax=alpha_axis,label=r'$x_{0}$',valmin=2,valmax=4,valinit=2,orientation='vertical')
alpha_slider.on_changed(update)

#Instantiate x initial slider and add event listener
x_0_axis = fig.add_axes([.16,0,.705,.03])
x_0_slider = Slider(ax=x_0_axis,label=r'$x_{0}$',valmin=.0001,valmax=.9999,valinit=.5)
x_0_slider.on_changed(update)
x_0_slider.on_changed(gen_bif_plot)
#Instantiate plot
update(1)

#plot :3
plt.show()














