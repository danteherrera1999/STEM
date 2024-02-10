import numpy as np
import matplotlib.pyplot as plt

# This code demonstrates how to calculate the discrete Fourier transform via the signal correlation method
# This is a great method to use if you don't know that fft exists or you want your code to perform poorly

#Discretization parameters
sr = 44100
N = 128

def ndfreqs(S):
    return np.array([i/S for i in range(int(S/2+1))])

def DFT_correl(s):
    N = s.size
    F = ndfreqs(N)
    B = np.array([np.correlate(np.cos(2*np.pi*f*np.arange(N)),s) for f in F]+[np.correlate(np.sin(2*np.pi*f*np.arange(N)),s) for f in F])
    B = 2 /N * B.flatten()
    B[0] /= 2
    B[-1] /= 2
    return (N,F,B)

#BUILD FUNCTION (FOR TESTING DEF)
dd = np.arange(N)
signal = lambda i: np.sin(.25*2*np.pi * i/10) + np.sin(.2*2*np.pi * i/10) + np.sin(.3*2*np.pi * i/10) + np.cos(100*2*np.pi*i/10)

def synth(cd,B,F):
    T = np.array([np.concatenate((np.cos(F*t*2*np.pi),np.sin(F*t*2*np.pi))) for t in cd]).T
    return np.matmul(B,T)

def DFT_correl_plot(s):
    N,F,B = DFT_correl(s)
    CA,SA = B[:int(N/2)+1], B[int(N/2)+1:]
    fig, (ax1,ax2,ax3) = plt.subplots(1,3)
    ax1.set_title("Signal")
    ax2.set_title("Cosine")
    ax3.set_title("Sine")
    ax1.plot(np.arange(N),s,"ro",label="samples")
    cd = np.linspace(0,N,10000)
    ax1.plot(cd,synth(cd,B,F),label="Projection",ls="--")
    ax1.legend()
    ax2.plot(F*100,CA,'ro')
    ax3.plot(F*100,SA,'ro')
    fig.suptitle("Fourier Transform Via Correlation Weight Function")
    ax1.set_ylabel("Amplitude")
    ax2.set_ylabel("Weight Factor")
    ax3.set_ylabel("Weight Factor")
    ax1.set_xlabel("Sample")
    ax2.set_xlabel("Frequency (% Sample Rate)")
    ax3.set_xlabel("Frequency (% Sample Rate)")

DFT_correl_plot(signal(dd))
plt.show()
