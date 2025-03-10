# TravelEye
<p align="center">
  <img src="Images/GithubLogo.png" alt="drawing" width="400"/>
</p>

<p align="center">
  <img src="Images/traveleyeposter.jpg" alt="TravelEye Poster" width="600"/>
</p>


## About
TravelEye is a portable device which used radio frequency detection to find hidden surveillance devices.
This device is aimed towards travelers with any level of technical knowledge

TravelEye scans using a list that contains frequencies that are known to be associated with surveillance devices. Any frequencies that are found to be above a determined threshold are shown to the user as possible surveillance devices.
The user can then select one of the found signals and TravelEye will then perform a focused scan on just that frequency. It will continuously scan, updating the signal strength so the user can walk around and watch the strength of the signal change for different parts of a room.
The user can then go through a few questions and TravelEye can provide advice on how to locate and possibly disable the device.

*Created by Owen Campain, Adam Wisnewski, Jacob Philips, Erand Bizati*

This project was created for a capstone course (CSC355) at Kutztown University and was formally presented at Kutztown's Demo Day 2024

## Installation
### Materials
This device was made with one specific list of components; however, this project could be recreated with slightly different components and still function. Below are the generic components required for the project along with exact models used by the team in parenthesis.
- RTL-SDR (V3)
- Raspberry Pi (3B+)
- Raspberry Pi Battery (PiSugar S Plus)
- Touch Screen (Hosyond 7-inch HDMI)
- SMA Antenna (Bingfu BFN00419)
- Normal Open Button (Twidec Push Button 7mm) 

This project uses a custom 3D printed case. The STL file for printing can be found in the repository `TravelEyeCase.stl`. Black PLA filament was used for the final case. Case design is based on the exact parts used therefore, if any components are swapped out, the case might no longer fit all components

### Assembly
The following diagram shows the layout of all the device components within the case

<p align="center">
  <img src="Images/TEArchitecture.png" alt="drawing" width="400"/>
</p>

The screen is connected to the Raspberry Pi via HDMI. The screen is also powered by the Raspberry Pi by connecting a USB type A port of the Raspberry Pi to one of the micro-USB ports on the screen

The RTL SDR is connected to the Raspberry Pi via USB Type A. USB Type A male to female cable was used in order for the RTL-SDR to fit inside of the case, however the RTL-SDR could be connected directly.

The antenna is attached to the RTL-SDR using the SMA connector.

The power button uses the number 5 and 6 pin on the Raspberry Pi

### Software Requirements
The TravelEye program runs off the Raspberry Pi which should be running Raspbian OS. Before being able to run program though, there are a few dependencies that need to be installed first

- [RTL SDR Drivers](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pi-power-button](https://github.com/Howchoo/pi-power-button.git)

### Running TravelEye
One the device has been assembled and all software requirements have been installed, TravelEye is ready to run

First make sure that `TravelEye.py`, `multipleChoiceMenu.py`, `MultiSigDetection.py` are located in the same folder before running

You can then start the program by running `TravelEye.py`

## Making Scan Adjustments
Scanning for such a wide range of different frequencies can be a challenge

There are many small adjustments to how this device scans which can affect what devices are found

There are two things that can be easily changed which can affect how the device works in different scenarios. You can adjust these values to make the device better suit your environment

### **Search list**

  This is the list of all frequencies which TravelEye will scan for.
  This list is contained in `dangerousFrequencies.txt`.

  You can add or remove any frequencies on this list. Keep in mind that all values are in MHz. The effective frequency range this device can scan for is 24 – 1766 MHz
 
  *Caution: The length of the list affects the length of scans. Adding too many frequencies can slow down the scan time*.

### Threshold
  This value represents the strength of the signal for it to be considered found. TravelEye collects data for all signals that were on the search list, however it only shows signals that we found to be above the threshold. 
  This value can be changed to make TravelEye more or less sensitive for finding signals 

  This value is contained in `MultiSigDetection.py` using the `THRESHOLD` variable. The threshold is measured in decibels

  *Caution: The UI and threshold was adjusted to only show the most prominent signals in order to not overwhelm the user with too many signals which might not be relevant. Making the threshold too low may cause all signals to be displayed which could break the UI* 

## User Guide
Here are some basic instructions and information on using TravelEye

### Instructions:

**1. Tap Start to scan**

  Scans once for all device ranges
  
  Signal strength is measured in decibels
  
  The higher the value, the stronger the signal
  
**2. Tap a found frequency to begin a focused scan**

  The device will repeatedly scan for one signal
  
  Watch the signal strength change as you move around
  
  Use this to locate where the signal is strongest
  
**3. Tap next to answer some questions to help locate the device**

### FAQ

_How close to a device do you need to detect it?_

There is no exact range on how far TravelEye can detect, it mainly depends on the strength of the signal it is trying to detect.
Most hidden devices put out a strong enough signal that TravelEye can detect as long as you are in the same room.
There have been some cases where TravelEye can detect from another room, but that is not always consistent.

_Can TravelEye find any camera or microphone?_

No, Currently TravelEye is intended to find cameras and microphones made for surveillance purposes which use radio frequency to communicate. 
Cameras and microphones which use wired or Wi-Fi communication cannot be found.
Our team would love to expand TravelEye's capabilities in the future, but for now TravelEye focuses on a more niche group of devices.

_What should I do if I find a device and cannot disable it?_

It is recommended to research surveillance and recording laws for your state/country as well as contacting the manager of the location you are staying. 
Every situation is different, so it is important to find out your rights. In many places, the authorities can be contacted if your right to privacy is being violated.

### Demo
Here is quick demo of the TravelEye device
https://www.youtube.com/watch?v=QhOCgh7br6o
