import time
import pygame
from ctime_button import Button
import os

class switch(Button):
  def __init__(self, screen, rect, image, colorkey):
    Button.__init__(self, screen, rect, image, colorkey)
    self.powerState=False
    self.rpiPower(self.powerState)
    self.enabled=True
    self.buttonTime=time.time()
    self.lightTime=time.time()

  def checkOff(self):
    nTime = time.time()
    if self.powerState==True:
      if (nTime - self.lightTime) > 3600:
        self.powerState=False
        self.rpiPower(self.powerState)

  def checkButton(self):
    nTime = time.time()
    if self.enabled==False:
      if (nTime - self.buttonTime) > 15:
        self.enabled=True
        return True
    return False
    

  def check_click(self, pos):
    if self.enabled == False:
      return False

    retVal = Button.check_click(self, pos)

    if retVal == True:
      self.powerState = not(self.powerState)
      self.rpiPower(self.powerState)
      self.buttonTime=time.time()
      self.lightTime=time.time()
      self.enabled=False

    return retVal

  def rpiPower(self, state):
    if (os.uname()[1] == 'rpi21'):
      if state == True:
        os.system("sudo ./rpion.py")
      else:
        os.system("sudo ./rpioff.py")
    else:
      print("NOT A PI. New state: "+str(state))

