import numpy as np
import matplotlib.pyplot as plt

# This code generates a serial ASCII waveform. It should be noted that the plot shows only logic levels not actual voltage.
# For example, RS232 woulld be [3,13]V for a 1 bit and [-13,-3]V for a 0 bit and TTL would be 5V for a 1 bit, most UART also invert the signal. 
# The parity bit is a form of data validation that ensures that each data packet follows some rule, usually that the total number of 1 bits is even or odd.
# The actual playback speed of this waveform would depend on the baud rate of the system

start_bit = "0"
stop_bit = "1"
data_bits = 7
parity="EVEN"
#parity = "NONE"
#Mark parity not supported

def cc(chr,data_bits,parity):
	raw = format(ord(chr),'08b')[8-data_bits:]
	parity_bit = "" if parity=="NONE" else str(int((sum([int(x) for x in raw])%2==1) ^ (parity=="ODD")))
	return "".join( x+x for x in start_bit  + raw[::-1] + parity_bit + stop_bit)

str_to_wf = lambda input_string : np.invert(np.array(list("".join(['1']+[cc(input_char,data_bits,parity) for input_char in input_string]))).astype(bool)).astype(int)

# This is the input string
st = '#**PS\r'

serial_wf = str_to_wf(st)

plt.title('Signal')
plt.plot(serial_wf,drawstyle='steps-pre')
plt.legend()
plt.ylabel('Logic Level')
plt.xticks([],[])
plt.show()


