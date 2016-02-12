import time
import pygame
from ctimeButton import button
import os
#if (os.uname()[1] == 'rpi21'):
#  import RPi.GPIO as GPIO

class switch(button):
  def __init__(self, screen, rect, image, colorkey):
    button.__init__(self, screen, rect, image, colorkey)
    self.powerState=False
    self.rpiPower(self.powerState)
    self.enabled=True
    self.buttonTime=time.time()
    self.lightTime=time.time()

  def checkClick(self, pos):
    nTime = time.time()
    if self.enabled==False:
      if (nTime - self.buttonTime) > 10:
        self.enabled=True

    if self.powerState==True:
      if (nTime - self.lightTime) > 60:
        self.powerState==False
        self.rpiPower(self.powerState)

    if self.enabled == False:
      return False

    retVal = button.checkClick(self, pos)

    if retVal == True:
      self.powerState = not(self.powerState)
      self.rpiPower(self.powerState)
      self.buttonTime=time.time()
      self.lightTime=time.time()

    return retVal

  def rpiPower(self, state):
    if (os.uname()[1] == 'rpi21'):
      if state == True:
        os.system("sudo ./rpion.py")
      else:
        os.system("sudo ./rpioff.py")
    else:
      print("NOT A PI. New state: "+str(state))

