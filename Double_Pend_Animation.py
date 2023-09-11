#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# This script shows how a complex oscillation in 2 DOF can be decomposed into its normal modes
# This works because the normal modes are orthogonal, and create a vector space so that any system oscillation
# Can be described as a linear combination of these modes
# This is my solution to an example used several times throughout Howard Georgi's "The Physics of Waves"

#Constants and parameters
m = 1 #kg
g = 9.81 #m/s^2
k = 100
l = 1/1000 # 10 cm in m
M = np.array([[m,0],[0,m]])
K = np.array([[m*g/l+k,-k],[-l,m*g/l+k]])

# Undamped Frequency
w_1s = g/l
w_2s = g/l+2*k/m
w_1 = np.sqrt(w_1s)
w_2 = np.sqrt(w_2s)
W = np.array([[w_1,0],[0,w_2]])

# Normal Modes
A_1 = np.array([[1],[1]])
A_2 = np.array([[1],[-1]])
X_1 = lambda t,b_1,c_1: A_1 * (np.cos(w_1*t) * b_1 + np.sin(w_1*t) * c_1)
X_2 = lambda t,b_2,c_2: A_2 * (np.cos(w_2*t) * b_2 + np.sin(w_2*t) * c_2)
X = lambda t,b_1,b_2,c_1,c_2 : X_1(t,b_1,c_1) + X_2(t,b_2,c_2)

# Pendulum root position
P_0 = np.array([[-2],[2]])

###### INITIAL CONDITIONS ########

X_0 = np.array([[-3],[-1]])
Xp_0 = np.array([[2],[-1]])

# Calculate mode coefficients from initial conditions
S = np.array([A_1,A_2]).T
B = np.matmul(np.linalg.inv(S),X_0).flatten()
C = np.matmul(np.matmul(np.linalg.inv(S),Xp_0).flatten(),np.linalg.inv(W))
b1,b2 = B
c1,c2 = C

# Instantiate plot
fig,ax = plt.subplots()
ax.set_xlim(-5,5)
ax.set_ylim(-1,1)
spring = .05*np.sin(np.linspace(0,2*np.pi*10.5,1000))
spring[:50] = 0
spring[950:] = 0
ln = [ax.plot([X_0[0][0]],[0],'ro',c='r'),ax.plot([X_0[1][0]],[0],'ro',c='b'),ax.plot([(np.sum(X_0.flatten()))/2],[-.5],'ro',c='g',label="Normal Mode 1"),ax.plot(X_0.flatten(),[-.75,-.75],'ro',c='k',label="Normal Mode 2"),ax.plot([P_0[0][0],P_0[0][0]+X_0[0][0]],[.5,0],c='r',ls='--'),\
ax.plot([P_0[1][0],P_0[1][0]+X_0[1][0]],[.5,0],c='b',ls='--'),ax.plot(np.linspace(X_0[0][0]+P_0[0][0],X_0[1][0]+P_0[1][0],1000),spring)]
plt.legend()

# Main update function
def update(frame):
	x1_delta, x2_delta = X(frame*.001,b1,b2,c1,c2)
	x1_delta = x1_delta[0]
	x2_delta = x2_delta[0]
	x1 = P_0[0][0]+x1_delta
	x2 = P_0[1][0]+x2_delta
	x_av = (x1+x2)/2
	ln[0][0].set_xdata([x1])
	ln[1][0].set_xdata([x2])
	ln[2][0].set_xdata([x_av])
	ln[3][0].set_xdata([x_av-x1,x_av-x2])
	ln[4][0].set_xdata([P_0[0][0],x1])
	ln[5][0].set_xdata([P_0[1][0],x2])
	ln[6][0].set_xdata(np.linspace(x1,x2,1000))
	#quit()
	return ln

#Instantiate animation object
ani = FuncAnimation(fig,update,frames=np.arange(10000),interval=.1)

#plot :3
plt.show()
