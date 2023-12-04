import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

"""
This code is a visualizer for finding the Nth complex roots of 1
in the complex space, the roots e^(2j*pi*k/N) represent a rotation in the complex
plane. The Nth roots of 1 therefore represent complex numbers that will return a vector to the same position
after N consecutive rotations.
"""

V_0 = np.array(np.linspace(0,1,100)+0j)

# R: Rotations
# O: Order
# S: Slice

def v(R,O,S):
	tv = np.exp(2j*np.pi/O*R*S) * V_0
	return np.array([np.real(tv),np.imag(tv)])
	
fig,ax = plt.subplots()
ln = 0
def generate_slices(R,O):
	global ln
	ax.clear()
	ax.set_ylim(-1.1,1.1)
	ax.set_xlim(-1.1,1.1)
	ax.set_aspect(1)
	for s in range(O):
		ax.plot(*v(R,O,s),color='blue',zorder=0)
	ln, = ax.plot(*v(R,O,0),color='red',zorder=100)

def generate_sliders(O):
	global ax_R,ax_S,S_slider,R_slider
	try:
		ax_R.clear()
		ax_S.clear()
	except:pass
	S_slider = Slider(
    		ax=ax_S,
    		label="Slice",
    		valmin=0,
    		valmax=O,
    		valinit=1,
		valstep=1,
    		orientation="vertical"
	)
	R_slider = Slider(
    		ax=ax_R,
    		label="Rotations",
    		valmin=1,
    		valmax=O-1,
    		valinit=1,
		valstep=1,
    		orientation="vertical"
	)
	R_slider.on_changed(update_R)
	S_slider.on_changed(update_S)
ax_O = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
ax_R = fig.add_axes([0.06, 0.25, 0.0225, 0.63])
ax_S = fig.add_axes([0.02, 0.25, 0.0225, 0.63])
S_slider = 0
R_slider = 0
O_slider = Slider(
	ax=ax_O,
	label="Order",
	valmin=2,
	valmax=10,
	valinit=6,
	valstep=1,
    	orientation="vertical"
	)

def update_O(val):
	global S_slider,R_slider
	generate_sliders(O_slider.val)
	update_R(0)
	update_S(0)
def update_R(val):
	generate_slices(R_slider.val,O_slider.val)
	update_S(0)
def update_S(val):
	global ln
	nv = v(R_slider.val,O_slider.val,S_slider.val)
	ax.set_title(f"i={np.round(nv[0,-1],2)}+{np.round(nv[1,-1],2)}j")
	ln.set_data(*nv)

update_O(1)

O_slider.on_changed(update_O)

plt.show()











