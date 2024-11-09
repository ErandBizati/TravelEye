#runTests.py

#import TestFunctions as testF

import MultiSigDetection
import tkinter as tk
import sys
import ast

SEARCHLIST = MultiSigDetection.SEARCHLIST
TRESHOLD = MultiSigDetection.TRESHOLD
#inputList = []


#if len(sys.argv) > 1:
  # Read the argument and convert it to a list
#  inputList = ast.literal_eval(sys.argv[1])

#menu(inputList)

for freq in SEARCHLIST:
  try:
    # Call the scan function from MultiSigDetection for each frequency
    result = MultiSigDetection.scan(MultiSigDetection.sdr, freq, TRESHOLD)
    # If any signals were detected, append them to the result
    if result:
      for detected in result:
        freq_found, power = detected
        inputList.append((freq_found, power))
    

  except Exception as e:
    #scan_result += f"Error scanning {freq} MHz: {str(e)}\n"
    break


def menu(inputList):

  def yes1():
    question.config(text="Are you able to touch the device?")
    yes.config(command=yesTouch)
    no.config(command=noTouch)


  def no1():
    question.config(text="It could be hidden. \nCheck smoke alarms, power outlets, walls, lights, electronic devices, \ndecorative items like stuffed animals, and anything that looks out of place.\nDid you find anything?")
    yes.config(command=yes1)
    no.config(command=noSmoke)

  def noSmoke():
    question.config(text="Are there any windows or openings around you?")
    yes.config(command=yesWindow)
    no.config(command=noWindow)


  def yesTouch():
    if len(inputList) > 1:
      question.config(text="If you never gave consent for a camera or microphone to be where you are,\nyou may be allowed to disable it. Look for power buttons around the device. \nIf there is not one, see if it is connected to a power source like an outlet and unplug it.\nIf none of these options are possible, your best scenario may be to physically obstruct the camera \nso it cannot see you and muffle the sound by wrapping it in something like a towel.\n If it is a microphone, muffle the sound with something like a towel or blanket and be wary.\nThere seems to be another signal found, move onto the next?")
      yes.pack_forget()
      no.pack_forget()
      nextFrequency = tk.Button(buttons, text="Next", font=('Times New Roman', 18), command=nextFreq)
      nextFrequency.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)
    else:
      question.config(text="If you never gave consent for a camera or microphone to be where you are,\nyou may be allowed to disable it. Look for power buttons around the device. \nIf there is not one, see if it is connected to a power source like an outlet and unplug it.\nIf none of these options are possible, your best scenario may be to physically obstruct the camera \nso it cannot see you and muffle the sound by wrapping it in something like a towel.\n If it is a microphone, muffle the sound with something like a towel or blanket and be wary.")
      nextFrequency = tk.Button(buttons, text="Next", font=('Times New Roman', 18), command=rescan)
      yes.pack_forget()
      no.pack_forget()
      reset = tk.Button(buttons, text="Rescan", font=('Times New Roman', 18), command=rescan)
      reset.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)

  def noTouch():
    if len(inputList) == 1:
      question.config(text="If the device is a microphone, it may be impossible to stop it. \nLook for places it may be plugged into like outlets or holes in the wall and unplug it if possible.\nBe careful of what you say in the room\nIf it is a camera, try to cover the line of sight so that it cannot see you.\nIt still may be able to hear, so be careful.")
      yes.pack_forget()
      no.pack_forget()
      reset = tk.Button(buttons, text="Rescan", font=('Times New Roman', 18), command=rescan)
      reset.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)
    else:
      question.config(text="If the device is a microphone, it may be impossible to stop it. \nLook for places it may be plugged into like outlets or holes in the wall and unplug it if possible.\nBe careful of what you say in the room\nIf it is a camera, try to cover the line of sight so that it cannot see you.\nIt still may be able to hear, so be careful.\nAnother frequency was found, move onto that one?")
      yes.pack_forget()
      no.pack_forget()
      nextFrequency = tk.Button(buttons, text="Next", font=('Times New Roman', 18), command=nextFreq)
      nextFrequency.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)


  def yesWindow():
    if len(inputList) == 1:
      question.config(text="Try to cover any windows or openings near you.\nThis may be where you are being monitored from.\nBlock your windows as well as you can.")
      yes.pack_forget()
      no.pack_forget()
      reset = tk.Button(buttons, text="Rescan", font=('Times New Roman', 18), command=rescan)
      reset.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)
    else:
      question.config(text="Try to cover any windows or openings near you.\nThis may be where you are being monitored from.\nBlock your windows as well as you can.\nAnother frequency was found, move onto that one?")
      yes.pack_forget()
      no.pack_forget()
      nextFrequency = tk.Button(buttons, text="Next", font=('Times New Roman', 18), command=nextFreq)
      nextFrequency.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)


  def noWindow():
    if len(inputList) == 1:
      question.config(text="There may be a false signal or it is well hidden. \nKeep searching or scan again.")
      yes.pack_forget()
      no.pack_forget()
      reset = tk.Button(buttons, text="Rescan", font=('Times New Roman', 18), command=rescan)
      reset.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)
    else:
      question.config(text="There may be a false signal or it is well hidden. \nKeep searching or scan again.\nAnother frequency was found, move onto that one?")
      yes.pack_forget()
      no.pack_forget()
      nextFrequency = tk.Button(buttons, text="Next", font=('Times New Roman', 18), command=nextFreq)
      nextFrequency.pack(side=tk.LEFT, padx=25)
      quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
      quit_button.pack(padx=25)


  def rescan():
    menu(inputList)

  def nextFreq():
    inputList.remove(inputList[0])
    menu(inputList)

  if len(inputList) != 0: 
    result = inputList[0]
  else:
    result = (-1, -1)




  text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 16, "bold")}
  title_text_style = {"fg": "lime", "bg": "black", "font": ("Courier", 28, "bold")}


  root = tk.Tk()
  root.attributes("-fullscreen", True)  # Enable full-screen mode
  root.configure(bg="black")  # Set background color to black

  count = 0

  root.geometry("650x300")

  resultString = ''


  #list of extremely hostile frequencies
  xHostileList = [37.6000,49.8300,49.8550,49.8900,139.6000,140.0000,140.8500,143.5000,146.5350,146.5356,148.0050,164.4625,164.8625,166.6625,166.8625,168.0000,168.8000,169.4450,169.5050,170.1000,170.2450,170.3050,170.4875,170.9750,171.0450,171.1050,171.4500,171.6000,171.8250,171.8450,171.9050,172.0000,172.2000,172.8875,172.8875,173.3500,175.0200,184.8500,190.6000,203.0000,221.5000,224.5000,303.6150,303.8250,304.2450,304.2614,310.0000,314.3750,314.8500,315.0000,321.9850,391.2050,392.7280,398.6050,399.0300,399.4550,414.9800,416.2500,416.8450,418.0000,420.5440,423.1250,427.1250,427.4750,427.8250,428.6350,429.5050,433.9200,439.2500,499.9700,499.9750,673.9350,1310.0000,1350.0000,1521.3068,1572.0350]

  resultString += f'A frequency was found at {result[0]} MHz\n'
  #very long list of possibilities
  if float(result[0]) in xHostileList:
      label = tk.Label(root, text="Threat: EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
  #20-45
  elif float(result[0]) >= 20 and float(result[0]) < 45:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The device is likely an old camera or microphone.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #45-50
  elif float(result[0]) >= 45 and float(result[0]) < 50:
    label = tk.Label(root, text="Threat: EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. This is in the range of a list of devices that can be very likely for surveillance devices. \nIt can be a camera or a microphone.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #45-88
  elif float(result[0]) >= 45 and float(result[0]) < 88:
    label = tk.Label(root, text="Threat: High", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. This is in the range of a list of devices that can be very likely for surveillance devices.\n It can be a camera or a microphone.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #88-108
  elif float(result[0]) >= 88 and float(result[0]) < 108:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is likely for eavesdropping devices \nlike microphones or crystal controlled devices.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #108-135
  elif float(result[0]) >= 108 and float(result[0]) < 135:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is likely to be a low cost device for eavesdropping. \nMicrophone is likely.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #135-150
  elif float(result[0]) >= 135 and float(result[0]) < 150:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is where thousands of eavesdropping devices are used. \nBe very wary of a microphone or other devices such as kit bugs.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #150-175
  elif float(result[0]) >= 150 and float(result[0]) < 175:
    label = tk.Label(root, text="Threat: EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is very popular for wireless microphones.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #175-200
  elif float(result[0]) >= 175 and float(result[0]) < 200:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is popular for wireless microphones.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #200-225
  elif float(result[0]) >= 200 and float(result[0]) < 225:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is very popular for eavesdropping devices. \nBe wary of anything nearby.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #225-300
  elif float(result[0]) >= 225 and float(result[0]) < 300:
    label = tk.Label(root, text="Threat: Low", **text_style)
    label.pack(pady=5)
    resultString += '. The range this frequency is in is mainly for the military. \nIt is unlikely there is a device, but if there is it is a low power device.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #300-365
  elif float(result[0]) >= 300 and float(result[0]) < 365:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is mainly used for military purposes, \nbut there are some possibilities of devices watching or listening.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #365-420
  elif float(result[0]) >= 365 and float(result[0]) < 400:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in has many newer eavesdropping devices. \nBe careful when talking.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #420-450
  elif float(result[0]) >= 420 and float(result[0]) < 450:
    label = tk.Label(root, text="Threat: High to EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is can be very dangerous. \nIf between 433 MHz and 434 MHz it is very likely to be a device.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #450-470
  elif float(result[0]) >= 450 and float(result[0]) < 470:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is very popular for long range eavesdropping, \nyou may not find the device.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #470-700
  elif float(result[0]) >= 470 and float(result[0]) < 700:
    label = tk.Label(root, text="Threat: Low", **text_style)
    label.pack(pady=5)
    resultString += '. The range this frequency is in is not very popular. \nIf there is a device it could be a low power microphone'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #700-800
  elif float(result[0]) >= 700 and float(result[0]) < 800:
    label = tk.Label(root, text="Threat: EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is very popular for wireless microphones.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #800-900
  elif float(result[0]) >= 800 and float(result[0]) < 900:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is popular for eavesdropping devices.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #900-928
  elif float(result[0]) >= 900 and float(result[0]) < 928:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is very popular for spy shop toys. \nIt is likely there is one nearby.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #928-1000
  elif float(result[0]) >= 928 and float(result[0]) < 1000:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is mainly used by high end equipment. \nCameras and microphones are possibly nearby.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #1000-1350
  elif float(result[0]) >= 1000 and float(result[0]) < 1350:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is popular for video and ultra-miniature audio devices.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #1350-1500
  elif float(result[0]) >= 1350 and float(result[0]) < 1500:
    label = tk.Label(root, text="Threat: Medium", fg="yellow", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is moderately used. \nIt can be a camera or a microphone.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #1500-1700
  elif float(result[0]) >= 1500 and float(result[0]) < 1700:
    label = tk.Label(root, text="Threat: Low", **text_style)
    label.pack(pady=5)
    resultString += '. The range this frequency is in is where a minor amount of activity is found. \nIt is less likely there is a device nearby.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #1700-2000
  elif float(result[0]) >= 1700 and float(result[0]) < 2000:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is has a large amount of audio and video devices. \nBe wary of cameras and microphones.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  #2000-2300
  elif float(result[0]) >= 2000 and float(result[0]) < 2300:
    label = tk.Label(root, text="Threat: High", fg="orange", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is used by spyshop toys. \nBe wary of ultra-low powered cameras.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  # >2400
  elif float(result[0]) >= 2400:
    label = tk.Label(root, text="Threat: EXTREME", fg="red", bg="black", font=("Courier", 16, "bold"))
    label.pack(pady=5)
    resultString += '. The range this frequency is in is where millions of devices are. \nCameras are very likely to be nearby.'
    secondLabel = tk.Label(root, text=resultString, **text_style)
    secondLabel.pack(pady=5)
  elif float(result[0]) == -1:
    label = tk.Label(root, text="No signal was found.\nThe likelihood of a device is very low.\nYou can either scan again or exit.", **text_style)
    label.pack(pady=5)

  if result[0] == -1:
    buttons = tk.Frame(root)
    buttons.pack(pady=25)
    reset = tk.Button(buttons, text="Rescan", font=('Times New Roman', 18), command=rescan)
    reset.pack(side=tk.LEFT, padx=25)
    quit_button = tk.Button(buttons, text="Quit", font=('Times New Roman', 18), command=root.destroy)
    quit_button.pack(padx=25)
    root.mainloop()
  else:

    question = tk.Label(root, text="Can you see the device that is monitoring you?", **text_style)
    question.pack(pady=10)

    buttons = tk.Frame(root)
    buttons.pack(pady=25)

    yes = tk.Button(buttons, text="Yes", font=('Times New Roman', 18), command=yes1)
    yes.pack(side=tk.LEFT, padx=25)

    no = tk.Button(buttons, text="No", font=('Times New Roman', 18), command=no1)
    no.pack(padx=25)

    root.mainloop()

if __name__ == "__main__":
  inputList = []
  menu(inputList)
