import time
import pygame
from ctimeButton import button
import os
if (os.uname()[1] == 'rpi21'):
  import RPi.GPIO as GPIO

class switch(button):
  def __init__(self, screen, rect, image, colorkey):
    button.__init__(self, screen, rect, image, colorkey)
    self.powerState=False
    self.rpiPower(self.powerState)

  def checkClick(self, pos):
    retVal = button.checkClick(self, pos)

    if retVal == True:
      self.powerState = not(self.powerState)
      self.rpiPower(self.powerState)

    return retVal

  def rpiPower(self, state):
    if (os.uname()[1] == 'rpi21'):
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(18, GPIO.OUT)
      GPIO.output(18, state)
    else:
      print("NOT A PI. New state: "+str(state))
