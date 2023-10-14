# Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import hbar, m_e, pi
from matplotlib.animation import FuncAnimation

# This simple animation shows the time evolution of the wave function of a particle subject to a delta function potential
# The particle in this animation is bound, the delta function potential has only one energy level that corresponds to a bound state


P= 1000 # Number of points in the domain
m = hbar # Particle Mass, hbar in this case
ts = 1/20 # This adjusts how fast the animation sweeps through time
width = 5 # Domain Width
alpha = 1E-34 # delta function "strength"


E = lambda alpha,m : - m * alpha **2 / 2 / hbar ** 2 # Bound state energy level
psi = lambda alpha,x: np.sqrt(m * alpha) / hbar * np.exp(-np.abs(x)*m * alpha / (hbar ** 2 )) # Time-independent Schrodinger Equation solution
phi = lambda alpha,m,t: np.exp(-1j * E(alpha,m) / hbar * t) # Time-dependent Schrodinger Equation solution
Psi = lambda alpha,m,t,x: psi(alpha,x) * phi(alpha,m,t) # Wave function of the particle
Prob = lambda Psi_data,width : (np.dot(np.conjugate(Psi_data),Psi_data)*2*width/P).real # Probability of finding particle inside the well (should always be one)
x_exp = lambda Psi_data,a,x : (np.dot(np.conjugate(Psi_data),x*Psi_data)*2*width/P).real # Expectation Value of position, numerical integral, not perfect, but certainly a lot easier :3 
# note: the value above should always be entirely real, the ".real" here is used only to convert the answer from a complex datatype for formatting purposes


# Plot Initialization
fig, ax = plt.subplots()
domain = np.linspace(-width,width,P)
lines = [ax.plot(domain,Psi(alpha,m,0,domain).real)[0],ax.plot(domain,Psi(alpha,m,0,domain).imag)[0],ax.plot(0,0,"ro",label=r"$<x>$")[0]]
L=ax.legend(loc=1)
ax.set_ylim(-1,1)
ax.set_xlim(-width,width)
ax.set_ylabel(r'$\Psi(x,t)$',rotation=0)
ax.set_title('Time Evolution Of '+r"$\Psi(x,t) = \frac{\sqrt{m\alpha}}{\hbar}e^{-\frac{m\alpha|x|}{\hbar^2}}e^{\frac{im\alpha^2 t}{2\hbar^3}}$")


# Main Animation Update Function
def update(frame):
	Psi_data = Psi(alpha,m,frame*ts,domain) # Gaussian Wave Packet
	xexp = x_exp(Psi_data,width,domain)
	lines[0].set_ydata(Psi_data.real)
	lines[1].set_ydata(Psi_data.imag)
	lines[2].set_xdata([xexp])
	L.get_texts()[0].set_text(r"$<x>:$ "+"{:.3f}".format(xexp)) # This breaks blit feature
	return lines

# Initialize Animation Object
ani = FuncAnimation(fig,update,interval=1,frames=1000)

# Show :3
plt.show()
