#-------------------#
# File: MultiSigDetection.py 
# Authors: Owen Campain
# Purpose: Intializes rtlsdr and provides scanning for a range of radio frequencies
#-------------------#
from pylab import *
from rtlsdr import *
import math
import numpy

# List of freq to search for
SEARCHLIST = [37.6000,49.8300,49.8550,49.8900,139.6000,140.0000,140.8500,143.5000,146.5350,146.5356,148.0050,164.4625,164.8625,166.6625,166.8625,168.0000,168.8000,169.4450
,169.5050,170.1000,170.2450,170.3050,170.4875,170.9750,171.0450,171.1050,171.4500,171.6000,171.8250,171.8450,171.9050,172.0000,172.2000,172.8875,172.8875
,173.3500,175.0200,184.8500,190.6000,203.0000,221.5000,224.5000,303.6150,303.8250,304.2450,304.2614,310.0000,314.3750,314.8500,315.0000,321.9850,391.2050
,392.7280,398.6050,399.0300,399.4550,414.9800,416.2500,416.8450,418.0000,420.5440,423.1250,427.1250,427.4750,427.8250,428.6350,429.5050,433.9200,439.2500
,499.9700,499.9750,521.3068,572.0350,673.9350]
# Value for a signal to be found present
TRESHOLD = -15

#initializes rtlsdr
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.gain = 4

#-------------------#
# Name: Scan
# Description: Using an rtlsdr, scans a frequency range. Returns all signals that are found to be above the given threshold.
# Parameters: rtl - rtlsdr object used to scan
#	      int freq - frequency in MHz to be set as the center for the scan
#             int threshold - value in dB for a signal to be considered present
# Return: list of all found frequencies
#-------------------#
def scan(rtl, freq, threshold):
	#offsets the center to account for I/Q overlap spikes
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
	
	#looks for frequencies that are within 0.1 MHz of eachother and keeps the highest. This reduces the amount of frequencies which are from the same source
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
	
