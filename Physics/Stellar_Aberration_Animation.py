#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# This animation demonstrates how stellar aberattion effects the apparent position of a star in the night sky as the earth moves around the sun

#Constants
c = 3E8 # speed of light m/s
N = 1000
ly = c * 365 * 3600 * 24 # light year in meters
theta_0 = 30 # stellar angle degrees
d = 100 * ly # distance to star
R_O = 1.496E11 # Earth orbit in meters
v_m = 29780
d2r = np.pi / 180


dv = lambda phi: -np.sin(phi * d2r) * v_m * np.sin(theta_0 * d2r) / c
dh = lambda phi: np.cos(phi * d2r) * v_m / c 


scale = 180 / np.pi * 3600 #scale factor #current converts to arcseconds

phis = np.linspace(0,720,N)

H = dh(phis) * scale
V = dv(phis) * scale
a_v = round(np.max(V)-np.min(V),2)
a_h = round(np.max(H)-np.min(H),2)


# Set up plot
fig, ax = plt.subplots()
lines = [ax.plot([],[])[0],ax.plot([],[],'ro', label=r"$\alpha_{vertical}: $"+str(a_v)+r"$''$"+"\n"r"$\alpha_{horizontal}: $"+str(a_h)+r"$''$"+"\n"+r"$\theta_{0}: $"+str(round(theta_0,2)))[0]]
ax.set_aspect(1)
ax.legend()

ax.set_title("Stellar Aberration")
ax.set_ylim(-25,25)
ax.set_xlim(-25,25)
def update(i):
	lines[0].set_data(np.roll(H,200-i)[:200],np.roll(V,200-i)[:200])
	lines[1].set_data([H[i]],[V[i]])
	return lines

#Instantiate animation object
ani = FuncAnimation(fig,update,interval=.01,frames=N)


#plot :3
plt.show()





