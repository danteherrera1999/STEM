# Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import hbar, m_e, pi
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

P= 1000 # Number of points in the domain
m = m_e # Particle Mass, mass of electron in this case
k = (36*m) # Restoring force
w = np.sqrt(k/m) # Natural Frequency
ts = np.pi / 80 # This adjusts how fast the animation sweeps through time
width = .02 # Domain Width

E_n = lambda n,w: (1 / 2  + n) * hbar * w # Energy associated with the Nth stationary state
psi_0 = lambda m,w,x : (m * w / pi / hbar) ** ( 1 / 4 ) * np.exp( - (m * w) / (2 * hbar) * x ** 2) # First solution to the time independent Schrodinger Equation
psi_1 = lambda m,w,x : np.sqrt(2 * m * w / hbar) * x * psi_0(m,w,x) # Second solution to the time independent Schrodinger Equation
Psi_0 = lambda m,w,x,t : psi_0(m,w,x) * np.exp(-1j*E_n(0,w)/hbar*t) # First Stationary State
Psi_1 = lambda m,w,x,t : psi_1(m,w,x) * np.exp(-1j*E_n(1,w)/hbar*t) # Second Stationary State
Psi_01 = lambda m,w,x,t : 1 / np.sqrt(2) * (Psi_0(m,w,x,t)+Psi_1(m,w,x,t)) # Wave Equation, in this case an equal superposition of the first 2 basis states
Prob = lambda Psi_data,width : (np.dot(np.conjugate(Psi_data),Psi_data)*2*width/P).real # Probability of finding particle inside the well (should always be one)
x_exp = lambda Psi_data,a,x : (np.dot(np.conjugate(Psi_data),x*Psi_data)*2*width/P).real # Expectation Value of position, numerical integral, not perfect, but certainly a lot easier :3 
# note: the value above should always be entirely real, the ".real" here is used only to convert the answer from a complex datatype for formatting purposes


# Plot Initialization
fig, ax = plt.subplots()
domain = np.linspace(-width,width,P)
lines = [ax.plot(domain,Psi_01(m,w,domain,0).real)[0],ax.plot(domain,Psi_01(m,w,domain,0).imag)[0],ax.plot(.5,0,"ro",label=r"$<x>$")[0]]
L=ax.legend(loc=1)
ax.set_ylim(-15,15)
ax.set_xlim(-width,width)
ax.set_ylabel(r'$\Psi(x,t)$',rotation=0)
ax.set_title('Time Evolution Of '+r"$\Psi(x,t) = \frac{1}{\sqrt{2}}(\psi_0(x)\phi_0(t)+\psi_1(x)\phi_1(t))$")

#Instantiate mass slider and add event listener, this allows a user to modify the mass of the particle during the animation
mass_axis = fig.add_axes([.2,.02,.7,.03])
mass_slider = Slider(ax=mass_axis,label="Mass "+r"($m_e$)",valmin=.1,valmax=5,valinit=2.5)

# Main Animation Update Function
def update(frame):
	m = mass_slider.val * m_e
	w = np.sqrt(k/m)
	Psi_data = Psi_01(m,w,domain,frame*ts) # Superposition of first 2 basis states
	xexp = x_exp(Psi_data,width,domain)
	lines[0].set_ydata(Psi_data.real)
	lines[1].set_ydata(Psi_data.imag)
	lines[2].set_xdata([xexp])
	L.get_texts()[0].set_text(r"$<x>:$ "+"{:.3f}".format(xexp)) # This breaks blit feature
	return lines

# Initialize Animation Object
ani = FuncAnimation(fig,update,interval=1,frames=10000)

# Show :3
plt.show()

