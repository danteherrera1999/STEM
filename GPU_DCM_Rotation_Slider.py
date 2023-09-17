#This example shows 3d rotations as performed gpu
import numpy as np
from numpy import cos,sin,pi
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import torch as t

# Sets pytorch to perform calculations on the gpu
cuda = t.device('cuda')

# Constant to convert degrees to radians
d2r=pi/180
# Generates a direction cosine matrix based on 3 euler angles, then converts it to a tensor and moves it to the gpu
DCM_tensor = lambda theta,phi,psi: t.matmul(t.matmul(t.tensor([[t.cos(psi),-t.sin(psi),0],[t.sin(psi),t.cos(psi),0],[0,0,1]]),t.tensor([[t.cos(phi),0,t.sin(phi)],[0,1,0],[-t.sin(phi),0,t.cos(phi)]])),t.tensor([[1,0,0],[0,t.cos(theta),-t.sin(theta)],[0,t.sin(theta),t.cos(theta)]])).to(cuda)
# Rotates any 3d dataset by the above DCM on the gpu
rot_gpu=  lambda data,theta,phi,psi: t.matmul(DCM_tensor(theta,phi,psi),data) # data = [xs,ys,zs]

# Generates cube, cheeky awful one line nice
generate_cube = lambda pps,width: [t.cat([side.T]+[rot_gpu(side,*rotation).T for rotation in t.tensor([[90,0,0],[180,0,90],[-90,0,0],[0,90,0],[0,-90,0]])*d2r]).T for side in [t.stack((t.flatten(t.linspace(-width/2,width/2,int(np.sqrt(pps))).repeat(int(np.sqrt(pps)),1)),t.flatten(t.linspace(-width/2,width/2,int(np.sqrt(pps))).repeat(int(np.sqrt(pps)),1).T),t.tensor([width/2]).repeat(int(np.sqrt(pps))**2))).to(cuda)]][0]
cube = generate_cube(1000,1) #Generates the 3 dimensional points for a cube, the first argument is the number of points per side, the second argument is the width of each side

# Instantiates plot
fig, ax = plt.subplots()
ax.set_ylim(-1,1)
ax.set_xlim(-1,1)
# Instantiates cube object in plot and projects it to 2 dimensions
cube_data, = ax.plot(*rot_gpu(cube,*t.tensor([0,0,0]))[:2].cpu(),'ro',alpha=.1,color='b')
ax.set_aspect('equal')

# Theta slider
theta_axis = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
theta_slider = Slider(
    ax=theta_axis,
    label=r"$\theta$",
    valmin=-180,
    valmax=180,
    valinit=0,
    orientation="vertical"
)
# Phi slider
phi_axis = fig.add_axes([0.06, 0.25, 0.0225, 0.63])
phi_slider = Slider(
    ax=phi_axis,
    label=r"$\phi$",
    valmin=-180,
    valmax=180,
    valinit=0,
    orientation="vertical"
)
# Psi slider
psi_axis = fig.add_axes([0.02, 0.25, 0.0225, 0.63])
psi_slider = Slider(
    ax=psi_axis,
    label=r"$\psi$",
    valmin=-180,
    valmax=180,
    valinit=0,
    orientation="vertical"
)

# Main update function
def update(val):
	theta_new = theta_slider.val * d2r
	phi_new = phi_slider.val * d2r
	psi_new = psi_slider.val * d2r
	#rotates cube data set by new values on the gpu, then moves the new dataset to the cpu and plots the 2d projection
	cube_data.set_data(*rot_gpu(cube,*t.tensor([theta_new,phi_new,psi_new]).float())[:2].cpu())

# Slider event listeners
theta_slider.on_changed(update)
phi_slider.on_changed(update)
psi_slider.on_changed(update)

#plot :3
plt.show()
