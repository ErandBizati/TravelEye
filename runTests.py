#runTests.py

import TestFunctions as testF
import tkinter as tk


class multipleChoiceMenu:

  def __init__(self, freq):

    if freq[0] != 433.92:
      raise Exception("No Frequency Found.")

    self.root = tk.Tk()

    self.count = 0

    self.root.geometry("650x300")

    self.canSee = False

    self.label = tk.Label(self.root, text="Can you see the device that is monitoring you?", font=('Times New Roman', 18))
    self.label.pack(padx=10, pady=10)

    self.buttons = tk.Frame(self.root)
    self.buttons.pack(pady=25)

    self.yes = tk.Button(self.buttons, text="Yes", font=('Times New Roman', 18), command=self.yes1)
    self.yes.pack(side=tk.LEFT, padx=25)

    self.no = tk.Button(self.buttons, text="No", font=('Times New Roman', 18), command=self.no1)
    self.no.pack(padx=25)

    self.root.mainloop()

  def yes1(self):
    self.canSee = True
    self.label.config(text="Are you able to touch the device?")
    self.yes.config(command=self.yesTouch)
    self.no.config(command=self.noTouch)


  def no1(self):
    self.label.config(text="Are there any windows or openings around you?")
    self.yes.config(command=self.yesWindow)
    self.no.config(command=self.noWindow)

  def yesTouch(self):
    self.label.config(text="Here is some information on how you may be able\n to cover or disable the device.")
    self.yes.pack_forget()
    self.no.pack_forget()

  def noTouch(self):
    self.label.config(text="Here is some information on how you may be able\n to cover the device or where it can see you.")
    self.yes.pack_forget()
    self.no.pack_forget()

  def yesWindow(self):
    self.label.config(text="Try to cover any windows or openings near you.\nThis may be where you are being monitored from.")
    self.yes.pack_forget()
    self.no.pack_forget()

  def noWindow(self):
    self.label.config(text="As of now, there may be a false signal.\n Please try again")
    self.yes.pack_forget()
    self.no.pack_forget()


multipleChoiceMenu(testF.scanWithResult())
