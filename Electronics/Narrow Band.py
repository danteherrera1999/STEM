import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import floor

"""
This script is for sizing the capacitors and resistors for a muiltiple feedback / narrow band active filter.
Adjust the central frequency and bandwidth below. Algorithm / Template circuit is from this video https://www.youtube.com/watch?v=UtnRQVeeLwM&t=937s
"""
f_0 = 500
B_W = 100


par = lambda vals: 1/np.sum(1/np.array(vals)) 
si_prefixes = dict(zip(np.arange(-5,6)*3,['f','p','n','μ','m','','k','M','G','T','P']))

def ns(n): # Number String
	i=floor((np.log10(n))/3)*3
	return str(round(n/10**i,2))+si_prefixes[i]

def get_template_vector(f_0,B_W):
	Q = f_0 / B_W
	w_t = 2 * np.pi * f_0
	R = np.array([Q,Q/(2*Q**2-1),2*Q,2*Q]) / w_t
	return R

def scale_by(R,s):
	vals = ''
	for i in range(R.size):
		vals += f"R{i+1}: {ns(R[i]*s)}Ω\n"
	for i in range(1,3):
		vals += f"C{i}: {ns(1/s)}F\n"
	return vals

def plot_scale_range(f_0,B_W):
	R = get_template_vector(f_0,B_W)
	N = int(1e3)
	scale = np.linspace(6,12,N)
	fig,ax = plt.subplots()
	Rs = [ax.plot(scale[::-1]*-1,np.log10(10**scale[::-1]*R[i]),label=f'R{i+1}')[0] for i in range(R.size)]
	Rmax = np.max(R)*10**np.max(scale)
	Rmax_log = np.log10(Rmax)
	ax.set_title(r"$f_0$: "+str(f_0)+r"Hz | $B_W$: " + str(B_W) + "Hz")
	ax.set_xlim(np.roll(-1*scale,1)[:2])
	ax.set_ylim([0,Rmax_log])
	ax.set_xlabel('log10(C)')
	ax.set_ylabel('log10(R)')

	vline, = ax.plot([-1,-1],[0,	Rmax_log],ls='--',c='r')
	
	rdata = ax.annotate(
    text='',
    xy=(0, 0),
    xytext=(10, 10), # distance from x, y
    textcoords='offset points',
    bbox={'boxstyle': 'round', 'fc': 'w'},
    zorder=100
	)

	def update(event):
		if event.inaxes is ax:
			x = event.xdata
			rdata.set_text(scale_by(R,10**(-1*x)))
			rdata.xy=(x,Rmax_log/2)
			vline.set_xdata([np.repeat(x,2)])
		fig.canvas.draw()


	onomve = plt.connect('motion_notify_event', update)
	plt.legend(loc=1)
	plt.show()


plot_scale_range(f_0,B_W)
