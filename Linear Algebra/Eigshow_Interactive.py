#imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyautogui as pag
import win32api

# This simple interactive code shows the relationship between eigenvalues and eigenvectors
# When the red dial and the black dial line up, A * x is a scalar multiple of x, 
# the exact scale factor is the eigenvalue, and the x vector at which this occurs is the eigenvalue
# Click and drag to move dials

#Due to interactivity with the mouse window constraints had to be enforced which may differ across computers
pad = .05
os = [7,112]
dpi = 96
fig, ax = plt.subplots(figsize=(900/dpi,900/dpi))
w, h = fig.canvas.get_width_height()
mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry("+%d+%d" % (0, 0))

#Matrix definition and initial x value
A = np.array([[3,1],[-1,7]])
x = np.array([1,0])
lines = [ax.plot([],[],color='red',label='x')[0],ax.plot([],[],c='k',label='A * x')[0],ax.plot([],[],"--",c='r')[0],ax.plot([],[],"--",c='k')[0],ax.text(1.2,1.75,'')]
unit = lambda vec: vec / np.sqrt(np.dot(vec,vec))
traces = [[x.copy()],[np.matmul(A,x)]]

#Finds eigenvalues for labeling later
evs = np.round(np.linalg.eig(A)[0],3)
get_closest_eig = lambda n: evs[np.argmin(abs(evs-n))]

#Plot setup
ax.set_ylim(-8,8)
ax.set_xlim(-4,4)
ax.set_aspect(1)
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.legend()

#Main update function
def update(i):
    global x,traces #Global variables... bite me
    #Mouse stuff
    if win32api.GetKeyState(0x01) < 0:
        x = ax.transData.inverted().transform((np.array([0, 1080]) - np.array(pag.position())) * np.array([-1, 1]) - os)
    Ax = np.matmul(A,x)
    try:
        if round(Ax[0] / x[0]) == round(Ax[1]/x[1]): #Checks if you are close to an eigenvector/value pair
            lines[4].set_text(f"Eigen Value: {get_closest_eig(Ax[0]/x[0])}")
        else:
            lines[4].set_text(f"No Eigenvalue")
    except:
        lines[4].set_text(f"No Eigenvalue")
    x = unit(x)
    Ax = np.matmul(A,x)
    traces[0].append(x.copy())
    traces[1].append(Ax.copy())

    if len(traces[0]) >= 30:
        traces[0] = traces[0][1:]
        traces[1] = traces[1][1:]
    lines[0].set_data(np.array([[0,0],x]).T)
    lines[1].set_data(np.array([[0,0],Ax]).T)
    lines[2].set_data(np.array(traces[0]).T)
    lines[3].set_data(np.array(traces[1]).T)
    return lines

#Instantiate animation object
myAnimation = FuncAnimation(fig, update, frames=500, interval=1, repeat=True)

#plot :3
plt.show()
