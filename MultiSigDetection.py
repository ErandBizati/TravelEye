#File: MultiSigDetection.py
from pylab import *
from rtlsdr import *
import math
import numpy

SEARCHLIST = [433.92, 49, 139, 143, 146, 169, 175,315]
TRESHOLD = -15

#initializes rtlsdr
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.gain = 4

def scan(rtl, freq, threshold):
	center = (freq + 0.024) * 1000000
	
	sdr.center_freq = center
	samples = sdr.read_samples(256*100)
	
	#use matplotlib to estimate and plot the PSD
	power,freqFound =psd(samples, NFFT=100, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
	
	#converts power data to decibels
	powerdB = [ 10*math.log10(x) for x in power ]
	
	#creates a tuple with each frequency and its dB which is over the threshold
	found = [(float(freqFound[powerdB.index(x)]),x) for x in powerdB if x > threshold]
	
	#removes center freq due to I/Q overlap effecting the dB
	for x in found:
		if(x[0] == center):
			found.remove(x)
	
	#this list will contain all found freq, with similar freq filtered out, keeping the strongest
	filtered = []
	i = 0
	
	while i < len(found):
		currentFreq, currentPower = found[i]
		maxPower = currentPower
		maxIndex = i
		
		j = i + 1
		while j < len(found) and found[j][0] - currentFreq <= 0.1:
			if found[j][1] > maxPower:
				maxPower = found[j][i]
				maxIndex = j
			j += 1
		filtered.append(found[maxIndex])
		i = j
	
	return(filtered)
	
detected = []

for x in SEARCHLIST:
	detected += scan(sdr, x, TRESHOLD)

print("\nFrequency |  dB\n--------------------------------")

for x in detected:
	print(f'{x[0]:10} | {x[1]:10}')
 


