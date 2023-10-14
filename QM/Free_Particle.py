# Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import hbar, m_e, pi
from matplotlib.animation import FuncAnimation

# This simple animation shows the time evolution of a free particle with a guassian wave function, (problem 2.21 in Griffiths)
# The derivation for this equation requires first solving the inverse fourier transform of the wave function at t=0 to find the continuous counterpart to what would be 
# the coefficients to the stationary states in the discrete case. The weighting function phi(k) in this case is essentially analogous to the frequency spectrum of the wave function. 
# Then you can plug this back into the integral for the wave function to get the time dependent result. Whats important here is that the free particle cannot be represented as a sum of a finite number of  
# states with discrete energy levels. This leads to the conclusion that a particle in a 0/constant potential cannot have a definite energy. I think this makes sense in the context of conservation of energy
# and the uncertainty principle. A particle in a 0/constant potential cannot have any potential energy, and thus 100% of its energy would be kinetic and massive.
# If the particle had a discrete energy level, you could exactly compute its momentum, which is not possible via the uncertainty principle.


P= 1000 # Number of points in the domain
m = hbar # Particle Mass, mass of electron in this case
ts = 1/200 # This adjusts how fast the animation sweeps through time
width = 5 # Domain Width
a = 1 # gaussian coefficient


gamma = lambda a,m,t : np.sqrt(1+(2j*hbar*a*t/m)) # Convenience paramater from "completing the square" in the wave function integral
Psi = lambda a,m,t,x : (2 * a / pi) ** (1 / 4) * 1 / gamma(a,m,t) * np.exp(-a*x**2 / gamma(a,m,t)**2) # Wave function of the particle
Prob = lambda Psi_data,width : (np.dot(np.conjugate(Psi_data),Psi_data)*2*width/P).real # Probability of finding particle inside the well (should always be one)
x_exp = lambda Psi_data,a,x : (np.dot(np.conjugate(Psi_data),x*Psi_data)*2*width/P).real # Expectation Value of position, numerical integral, not perfect, but certainly a lot easier :3 
# note: the value above should always be entirely real, the ".real" here is used only to convert the answer from a complex datatype for formatting purposes


# Plot Initialization
fig, ax = plt.subplots()
domain = np.linspace(-width,width,P)
lines = [ax.plot(domain,Psi(a,m,0,domain).real)[0],ax.plot(domain,Psi(a,m,0,domain).imag)[0],ax.plot(0,0,"ro",label=r"$<x>$")[0]]
L=ax.legend(loc=1)
ax.set_ylim(-1,1)
ax.set_xlim(-width,width)
ax.set_ylabel(r'$\Psi(x,t)$',rotation=0)
ax.set_title('Time Evolution Of '+r"$\Psi(x,t) = (\frac{2a}{\pi})^{\frac{1}{4}}(\frac{1}{\gamma})e^{-\frac{ax^2}{\gamma^2}}$")


# Main Animation Update Function
def update(frame):
	Psi_data = Psi(a,m,frame*ts,domain) # Gaussian Wave Packet
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

