# Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.constants import hbar,m_e,pi

# This simple animation shows the time evolution of a wave function in the infinite square well
# The wave function in this example is an equal parts superposition of the first 3 basis states
# I made while reading through Griffiths primarily to help me understand the role of stationary states in the construction of the wave function
# The orthogonal nature of the stationary states allows us to decompose the wave function into basis functions and generate the time evolution of the
# wave function from the time-independant Schrodinger equation solutions

# Constant Definitions
P = 10000 # Number of points for plots
a = 1 # Width of potential well
m = m_e # Mass of test particle (electron in this case)
ts = 2*np.pi # This just adjusts how fast the animation sweeps through time

# Function Definitions
k_n = lambda a,n : n * (pi/a) # Angular Frequency of the Nth sationary state
E_n = lambda a,n,m : (hbar ** 2 * pi ** 2 * n ** 2) / ( 2 * m * a ** 2 ) # Energy associated with the Nth stationary state
psi_n = lambda a,n,x: np.sqrt( 2 / a ) * np.sin( ( n * pi / a ) * x ) # Normalized solution to time independent Schrodinger equation for Nth state, these are essentially the basis functions with which we will build our wave function
phi_n = lambda a,n,m,t: np.exp( -1j *  E_n(a,n,m) / hbar * t) # Solution to space independent Schrodinger equation for Nth state, this contains the phase information of our stationary state
Psi_n = lambda a,n,m,x,t: psi_n(a,n,x)*phi_n(a,n,m,t) # Nth stationary state
Prob = lambda Psi_data,a : (np.dot(np.conjugate(Psi_data),Psi_data)*a/P).real # Probability of finding particle inside the well (should always be one)
x_exp = lambda Psi_data,a,x : (np.dot(np.conjugate(Psi_data),x*Psi_data)*a/P).real # Expectation Value of position, numerical integral, not perfect, but certainly a lot easier :3 
# note: the value above should always be entirely real, the ".real" here is used only to convert the answer from a complex datatype for formatting purposes

# Plot Initialization
fig, ax = plt.subplots()
domain = np.linspace(0,a,P)
lines = [ax.plot(domain,Psi_n(a,2,m,domain,0).real)[0],ax.plot(domain,Psi_n(a,2,m,domain,0).imag)[0],ax.plot(.5,0,"ro",label=r"$<x>$")[0]]
L=ax.legend(loc=1)
ax.set_ylim(-2,2)
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$\Psi(x,t)$',rotation=0)
ax.set_title('Time Evolution Of An Example Infinite Square Well Wave Function')

# Main Animation Update Function
def update(frame):
	Psi_data = 1 / np.sqrt(3) * (Psi_n(a,1,m,domain,frame*ts) + Psi_n(a,2,m,domain,frame*ts) + Psi_n(a,3,m,domain,frame*ts)) # Superposition of first 3 basis states
	xexp = x_exp(Psi_data,a,domain)
	lines[0].set_ydata(Psi_data.real)
	lines[1].set_ydata(Psi_data.imag)
	lines[2].set_xdata([xexp])
	L.get_texts()[0].set_text(r"$<x>:$ "+"{:.3f}".format(xexp)) # This breaks blit feature
	return lines

# Initialize Animation Object
ani = FuncAnimation(fig,update,interval=1,frames=10000)

# Show :3
plt.show()
