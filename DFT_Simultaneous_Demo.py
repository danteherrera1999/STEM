import numpy as np
import matplotlib.pyplot as plt

# This code demonstrates how to calculate the discrete Fourier transform via the simultaneous equations method
# This is a great method to use if you don't know that fft exists or you want your code to perform poorly

#Discretization parameters
sr = 44100
N = 128

def ndfreqs(S):
    return np.array([i/S for i in range(int(S/2+1))])

def DFT_simul(s):
    N = s.size
    F = ndfreqs(N)
    # Buil A Matrix
    A = []
    for j in range(N):
        A.append(np.concatenate((np.cos(F*j),np.sin(F[1:-1]*j))))
    A = np.array(A)
    B = np.linalg.solve(A, s)
    return (N,F,B)

dd = np.arange(N)
signal = lambda i: np.sin(.25*2*np.pi * i/10) + np.sin(.2*2*np.pi * i/10) + np.sin(.3*2*np.pi * i/10) + np.cos(100*2*np.pi*i/10)

def synth(cd,B,F):
    T1 = np.array([np.cos(F*t) for t in cd])
    T2 = np.array([np.sin(F[1:-1]*t) for t in cd])
    T = np.concatenate((T1,T2),axis=1).T
    return np.matmul(B,T)

def DFT_simul_plot(s):
    N,F,B = DFT_simul(s)
    CA,SA = B[:int(N/2)+1], np.concatenate(([0],B[int(N/2)+1:],[0]))
    fig, (ax1,ax2,ax3) = plt.subplots(1,3)
    ax1.set_title("Signal")
    ax2.set_title("Cosine")
    ax3.set_title("Sine")
    ax1.plot(np.arange(N),s,"ro",label="samples")
    cd = np.linspace(0,N,10000)
    ax1.plot(cd,synth(cd,B,F),label="Projection",ls="--")
    ax1.legend()
    ax2.plot(F*100,CA,"ro")
    ax3.plot(F*100,SA,"ro")
    fig.suptitle("Fourier Transform Via Simultaneous Equations")
    ax1.set_ylabel("Amplitude")
    ax2.set_ylabel("Weight Factor")
    ax3.set_ylabel("Weight Factor")
    ax1.set_xlabel("Samples")
    ax2.set_xlabel("Frequency (% Sample Rate)")
    ax3.set_xlabel("Frequency (% Sample Rate)")

DFT_simul_plot(signal(dd))
plt.show()
