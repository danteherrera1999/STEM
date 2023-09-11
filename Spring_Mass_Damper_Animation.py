#Imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Spring Mass Damper system response animation with a few different damping coefficients to demsonstrate the effect on the response

k = 5/2
m = 5/2


#Damped frequency of SMD system
w_d = lambda m,k,c: np.sqrt(-1 * (c ** 2 - (4 * m * k)) ) / 2 / m

#Time constant of SMD system
tau = lambda m,c: 2 * m / c
response = lambda t,m,k,c: np.exp((-1 / tau(m,c) * t)) * (np.sin(w_d(m,k,c) * t) + np.cos(w_d(m,k,c) * t))
dom = np.linspace(0, tau(m,1) * 5, 2000)

# Instantiate Plot
fig, ax = plt.subplots()
Rs = []
line = []
for c in np.arange(1,6,1):
    Rs.append(response(dom,m,k,c))
    line.append(ax.plot([0], [0],label=f"c: {c}, " + r"$4\tau$"+ f":{round(100*tau(m,c))/100*4}s",ls="--")[0])
Rs = np.array(Rs)
Rs /= np.max(np.abs(Rs))/100


ax.legend()
ax.set_title("Plot of Spring Mass Damper System Response")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Response (% Max Value)")
ax.set_ylim(-100,100)
ax.set_xlim(0,dom[-1])

#Main Update Function
def update(i):
    for z in range(len(line)):
        line[z].set_data(dom[0:i],Rs[z][0:i])
    return line

#Instantiate animation object
a = FuncAnimation(fig, update,interval=1, frames=2000,blit=True)

#plot :3
plt.show()