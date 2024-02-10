#imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# This is a short and sweet example of how a linear combination of sine and cosine components creates a phase offset sinusoidal wave
# While simple, this is a very powerful concept as it allows a general solution to the equation of motion for an oscillating system
# to include phase changes as simple coefficients to sine/cosine components

#Instantiate Plot
fig, ax = plt.subplots()
d = np.linspace(0,4*2*np.pi,10000)
c = lambda t: np.cos(t)
s = lambda t: np.sin(t)
x = lambda t,a,b: a * c(t) + b * s(t)
lines = [ax.plot(d,c(d),ls="--",label="Cosine"),ax.plot(d,s(d),ls="--",label="Sine"),ax.plot(d,x(d,1,1),label="Composite")]
legend = plt.legend()
ax.set_ylim(-5,5)

#Add axes and sliders
ax_a = fig.add_axes([.96,.25,.0225,.63])
ax_b = fig.add_axes([.92,.25,.0225,.63])
a_slider = Slider(ax=ax_a,label="cos",valmin=-10,valmax=10,valinit=1,orientation="vertical")
b_slider = Slider(ax=ax_b,label="sin",valmin=-10,valmax=10,valinit=1,orientation="vertical")

#Main update function
def update(dummy):
	lines[0][0].set_ydata(a_slider.val*c(d))
	lines[1][0].set_ydata(b_slider.val*s(d))
	lines[2][0].set_ydata(x(d,a_slider.val,b_slider.val))
	lines[2][0].set_label("hi")
	plt.legend()
	fig.canvas.draw_idle()

#Add slider event listeners
a_slider.on_changed(update)
b_slider.on_changed(update)

#plot :3
ax.set_ylabel('Amplitude')
plt.show()






