import numpy as np
import matplotlib.pyplot as plt



f = lambda z_0,z : np.sqrt((z_0/z)**2-1)


Z = np.linspace(0,np.pi*7/2,10000)

for i in range(4):
	zp = np.linspace(.00000001+i*np.pi,(i+1)*np.pi,1000)
	if i==0:
		plt.plot(zp,-1/np.tan(zp),c='blue',label=r"$-cot(z)$")
	else:
		plt.plot(zp,-1/np.tan(zp),c='blue')
for z_0 in [1,3,6,10]:
	plt.plot(Z,f(z_0,Z),label=rf"$z_0$: {z_0}")
plt.ylim(-1,4)
plt.legend()
plt.xticks([np.pi*i for i in range(0,5)],["0",r"$\pi$"]+[rf"{i}$\pi$" for i in range(2,5)])
plt.show()