import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter as gf
from numpy.fft import fft, ifft

# This script is a simple signal correction alogrithm. The intended signal is sent through, then the output is measured
# From this the transfer function of the system is calculated by dividing both signals in the frequency domain (equivalent to a deconvolution)
# With the system transfer function, it is possible to adjust the input signal such that the output signal is what you intended originally after going through the system
# This is a small demonstration of a script that has been very useful in the lab [which i wrote in labview ultimately :'( ] which can generate waveforms, measure with an oscilloscope, and then real time process
# The data to generate a new waveform which will give the desired output after going through an arbitrary system (e.g. a few pieces of instrumentation and an operational amplifier)

#Basically the entire math part of the code, a great deal of complicated math in one line courtesy of numpy and the fast fourier transform
dcquik = lambda S,O: ifft(fft(S)/(fft(O)/fft(S)))


N = 10000
k = np.zeros(1000)
k[int(k.size/2)] = 1
#Some arbitrary system transfer function generated here with a gaussian kernel 
G = np.convolve(gf(k,100),np.roll(np.arange(1000)/10000,200),'same')

#Signal
S = np.sin(np.pi*2*np.linspace(0,100,N))
S = np.where(S>0,S,0)
#Output Signal (after going through some arbitrary system represented by tranfer function 'G')
O = np.convolve(S,G,'same')
C = np.fft.fft(O)/np.fft.fft(S)
CW = np.fft.ifft(C,1000)
IC = dcquik(S.tolist(),O.tolist())
OC = np.convolve(IC,G,'same')

#Show Signals before and after adjustment
plt.figure()
plt.plot(S,label="Input")
plt.plot(O,label='Output')
plt.title('Signal Correction Program')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.plot(IC,'--',label='Corrected Input')
plt.plot(OC,'--',label='Corrected Output')
plt.legend()
plt.xlim(4000,4300)

#Show calculated Transfer function
#plt.figure()
#plt.plot(G)
#plt.plot(CW.real)
#plt.title('Transfer Function')

#plot :3
plt.show()


