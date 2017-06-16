#!/usr/bin/python

import pygame,sys,pygame.camera
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

class ctimeCamera:
  def __init__(self, sWidth, sHeight,path):
    self.sWidth=sWidth
    self.sHeight=sHeight
    self.gameState=2
    self.path = path

    pygame.camera.init()

    self.screen=pygame.display.set_mode((sWidth,sHeight))
    go_fullscreen()

    # Try displaying USB camera view
    self.usbCamera=False
    try:
      self.cam = pygame.camera.Camera("/dev/video0",(sWidth,sHeight))
      self.cam.start()
      self.usbCamera=True
    except:
      pass

    self.buttonExit = button(
                             self.screen,
                             (self.sWidth - 200,0,200,200),
                             "images/icons/StopButton.png",
                             (0,0,0)
                            )

    self.re_init()

  def updateCamera(self):
    if self.usbCamera == True:
      image = self.cam.get_image()
      imWidth=image.get_width()
      imHeight=image.get_height()
      self.screen.blit(image,(0,self.sHeight - imHeight))
      pygame.display.update()

    self.re_init()
    
  def checkExit(self, pos):
          if (self.buttonExit.checkClick(pos)):
                  self.cam.stop()
                  return True
          else:
                  return False

  def re_init(self):
    try:
      self.image=pygame.image.load("%s/CAMERA1.jpg" % (self.path)).convert()
      self.screen.blit(self.image,(0,0))
      imWidth=self.image.get_width()
      imHeight=self.image.get_height()
      try:
        self.image = pygame.image.load("%s/CAMERA2.jpg" % (self.path)).convert()
        self.screen.blit(self.image,(self.sWidth - imWidth,self.sHeight - imHeight))
      except:
        pass
    except:
      pass


