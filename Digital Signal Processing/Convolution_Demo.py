import numpy as np
import matplotlib.pyplot as plt
from time import time

# This code demonstrates how to calculate the convolution of two signals with simple array mapping
# Very neat, Very inefficient :)

# Step
N = 10000
# Maximum Time
T_M = 50*np.pi

dom = np.linspace(0,T_M,N)
dt = T_M / N

# Impulse Response
h = np.sin(dom)
#Flip and Attenuate
#h = np.array([-1])
M = h.size

# Input Signal
s = lambda t: np.cos(t)
s = s(dom)
sf = s[::-1]

# Weighted Impulse Response
hs = h * dt

# Convolution
def conv(hs,sf):
    Cs = []
    #Transient Rise
    for i in range(M):
        Cs.append(np.dot(hs[0:i+1],sf[N-1-i:]))

    #Flat Section
    if N-M >0:
        for i in range(M,N):
            Cs.append(np.dot(hs,sf[N-1-i:M-i-1]))

    #Transient Fall
    for i in range(1,M):
        Cs.append(np.dot(hs[i:], sf[0:M-i]))
    return np.array(Cs)

t0 = time()
Cs = conv(hs,sf)
tf = time()

#New domain
dn = np.concatenate((dom,np.linspace(dom[-1]+dt,dt*(M-1)+dom[-1],(M-1))))

# Runtime
print(f"This operation took: {round(1000*(tf-t0))}ms")

# Plots or it didn't happen
plt.title("Signal Response")
plt.plot(dn,np.convolve(s,h)*dt,"-.",label='numpy convolution')
plt.plot(dn,Cs,'--',label='convolution code')
plt.legend()

#plot :3
plt.show()
