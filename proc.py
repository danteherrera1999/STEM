import numpy as np
import matplotlib.pyplot as plt
import os
images_folder = "jello_cold"
os.chdir(images_folder)
data =  np.loadtxt(images_folder+'_COUNTS.csv',delimiter=',').astype(float).T

sapp_A = 2.85 / 19060 / 100**2 #surface area in M2 per pixel
sapp_B = 2.85 / 74313 / 100**2#surface area in M2 per pixel (phone)

sigma_A = np.sqrt(sapp_A)
sigma_B = np.sqrt(sapp_B)

Ds = np.array([1.34,1.45,.5,194])
rs = np.array([0.4866606494447088,0.4752804082866022,0.2619521029345805,0.3000923941569326])
R = lambda counts: np.sqrt(sapp_B * counts / np.pi) #Radius in m
stds = Ds/rs/2

stds[:2]*= sigma_A
stds[2:]*=sapp_B
stds *= (10 * 1000)**2
print(stds)

quit()
data = (data[data.T[0]<10000]).T
R2 = (R(data[1])*100)**2
a,b = np.polyfit(data[0][data[0]>4000],R2[data[0]>4000],1)

R2_f = lambda time: a*time+b
D = a/4
print(f"Diffusion Constant: {D}CM2/s")
d = np.linspace(data[0,0],data[0,-1],100000)

plt.ylabel(r"Radius ($cm^2$)")
plt.xlabel("Time (s)")
plt.plot(data[0],R2,'ro')
plt.plot(d,R2_f(d),'--',label=f"D: {np.round(D*1e6,2)} "+r"$\times 10^{-6} \ \frac{cm^2}{s}$")
plt.title(r"Diffusion Area V.S. Time (Red Dye at Room Temperature)")
plt.legend()
plt.show()



