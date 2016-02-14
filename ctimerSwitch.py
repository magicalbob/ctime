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
    

  def checkClick(self, pos):
    if self.enabled == False:
      return False

    retVal = button.checkClick(self, pos)

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
