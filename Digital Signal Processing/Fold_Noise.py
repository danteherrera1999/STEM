import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

"""
This is a simple demo of foldover noise in an undersampled system. If the frequency of a signal
is beyond the sample rate of the data acquisition system, it could still introduce lower
frequency noise into the collected signal as a function of the frequency of the noise source
and the sample rate of the hardware. Unfortunately, once this noise is digitized, there is no way to 
differentiate it from a true low frequency signal through software. Foldover noise can be reduced by
implementing hardware filters to lower the bandwidth of your input signal to only those frequencies 
which can be resolved by the analog to digital converter.
"""

# Signal is a simple sine function
signal = lambda t,f: np.sin(t * 2 * np.pi * f)
# This represents the discretized time sampling of an ADC
time_samps = lambda t_0, t_e, sr: np.arange(t_0,t_e,1/sr)


# Instantiate plot
fig, ax = plt.subplots()
ln = [ax.plot([],[],'--',label='Signal')[0],ax.plot([],[],c='r',label='Discretized')[0]]
period = 1 # Number of seconds to collect
ax.set_ylim(-1.2,1.4)
plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
plt.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
plt.title('Fold Over Noise')

#Instantiate frequency slider
axfreq = fig.add_axes([0.25, 0.01, 0.63, 0.0225])
freq_slider = Slider(ax=axfreq,label='Frequency (Hz)',valmin=1,valmax=200,valinit=50,valstep=1)

# Instantiate sample rate slider
axsr = fig.add_axes([0.25, 0.06, 0.63, 0.0225])
sr_slider = Slider(ax=axsr,label="Sample Rate (Hz)",valmin=2,valmax=200,valinit=51,valstep=1)

ax.legend(loc=1)
# Plot update function
def update(i):
	T = 1/sr_slider.val # Sample period
	window = (period*i+i*T,period*(i+1)+i*T) # Data collection window (shifts by 1 sample period every iteration to show dynamic signal)
	domain = np.linspace(*window,10000)
	domain_disc = time_samps(*window,sr_slider.val)
	ax.set_xlim(period*i+(i-1)*T,period*(i+1)+T*i)
	ln[0].set_data(domain,signal(domain,freq_slider.val))
	ln[1].set_data(domain_disc,signal(domain_disc,freq_slider.val)) # Update line
	return ln

# Instantiate animation
ani = FuncAnimation(fig,update,frames=10000,interval=1)

# Run
plt.show()

