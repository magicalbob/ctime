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

  def checkClick(self, pos):
    print("CLICK POWER")
    retVal = button.checkClick(self, pos)

    if retVal == True:
      self.powerState = not(self.powerState)
      self.rpiPower(self.powerState)

    return retVal

  def rpiPower(self, state):
    if (os.uname()[1] == 'rpi21'):
      if state == True:
        os.system("sudo /home/pi/ctime/rpion.py")
      else:
        os.system("sudo /home/pi/ctime/rpioff.py")
    else:
      print("NOT A PI. New state: "+str(state))
