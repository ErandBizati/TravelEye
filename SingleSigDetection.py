from pylab import *
from rtlsdr import *
import math

#initializes rtlsdr
sdr = RtlSdr()

#gets freq from user
freq = float(input("Enter Frequency to scan (in MHz)"))
freq = freq * 1000000
if(freq < 2.5e7 or freq > 1.7e9):
	print("Frequency is out of range (Min 25, Max 1700)")
	exit(1)

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = freq
sdr.gain = 4

#collects data
samples = sdr.read_samples(256*100)
sdr.close()

#use matplotlib to estimate and plot the PSD
power,freqFound =psd(samples, NFFT=100, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

#converts power data to decibels
powerdB = [ 10*math.log10(x) for x in power ] 

print(powerdB,'\n')
print(freqFound)

#creates and displays data graph
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')
show()
