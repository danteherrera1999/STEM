#library imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.widgets import Slider

#This simple code demonstrates the effect of damping coefficients and intial conditions on the response of a Van Der Pol Oscillator and Limit Cycle


#instantiate constants\initial conditions
a = 1
mu = .5
w_0 = 1
x_0,x_dot_0  = 3,0

#Van Der Pol equation
def vdp(t,X):
	x,x_dot = X
	return [x_dot,-mu*(x**2-a**2)*x_dot - x*w_0**2]	

#Set Time Domain
l,r = 0,100
t = np.linspace(l,r,1000)

#Generate figure and set bounds
fig, ax = plt.subplots()
ax.set_ylim(-5,5)
ax.set_xlim(-5,5)

#Initilize Solution
sol = lambda x_0,x_dot_0: solve_ivp(vdp,[l,r],[x_0,x_dot_0],t_eval=t)
s_0 = solve_ivp(vdp,[l,r],[x_0,x_dot_0],t_eval=t)
ln, = ax.plot(s_0.y[0],s_0.y[1])

# Make a vertically oriented slider to control the a value
ax_a = fig.add_axes([0.95, 0.25, 0.0225, 0.63])
a_slider = Slider(
    ax=ax_a,
    label="a",
    valmin=-10,
    valmax=10,
    valinit=1,
    orientation="vertical"
)

# Make a vertically oriented slider to control the mu value
ax_mu = fig.add_axes([0.93, 0.25, 0.0225, 0.63])
mu_slider = Slider(
    ax=ax_mu,
    label=r"$mu$",
    valmin=-10,
    valmax=10,
    valinit=1,
    orientation="vertical"
)

# Make a horizontal slider to control the x_0.
ax_x_0 = fig.add_axes([0.25, 0.04, 0.65, 0.03])
x_0_slider = Slider(
    ax=ax_x_0,
    label=r'$x_0$',
    valmin=-5,
    valmax=5,
    valinit=1,
)

# Make a horizontal slider to control the x_dot_0.
ax_x_dot_0 = fig.add_axes([0.25, 0.01, 0.65, 0.03])
x_dot_0_slider = Slider(
    ax=ax_x_dot_0,
    label=r'$\dot{x}_0$',
    valmin=-5,
    valmax=5,
    valinit=1,
)

#Main update function, this will update the plot when a slider is changed
def update(val):
	global a,mu
	a = a_slider.val
	mu = mu_slider.val
	s = sol(x_0_slider.val,x_dot_0_slider.val)
	ln.set_data(s.y[0],s.y[1])
	fig.canvas.draw_idle()

#Add event listener to sliders
x_0_slider.on_changed(update)
x_dot_0_slider.on_changed(update)
a_slider.on_changed(update)
mu_slider.on_changed(update)

#Add info
ax.set_title('Van Der Pol Oscillator Visualizer')
ax.set_ylabel(r'$\frac{dx}{dt}$',rotation=0,fontsize=25)
ax.set_xlabel(r'$x$',fontsize=25)
ax.xaxis.set_label_coords(.05,-.05)

#plot :3
plt.show()