import random

def scanWithResult():
	freq = 433.92
	ftype = "camera"
	result = (freq,ftype)
	return(result)
	
def scanWithoutResult():
	freq = None
	ftype = None
	result = (freq,ftype)
	return(result)
	
def scanWithTwoResult():
	freq1 = 433.92
	ftype1 = "camera"
	freq2 = 100
	ftype2 = "microphone"
	result1 = (freq1,ftype1)
	result2 = (freq2,ftype2)
	return(result1,result2)
	
def scan():
	random.seed()
	func = random.randrange(1,3,1)
	if(func == 1):
		return scanWithResult()
	if(func == 2):
		return scanWithoutResult()
	if(func == 3):
		return scanWithTwoResult()
