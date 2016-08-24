#!/usr/bin/python

import pygame,sys,pygame.camera
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

class ctimeCamera:
  def __init__(self, sWidth, sHeight):
    self.sWidth=sWidth
    self.sHeight=sHeight

    pygame.camera.init()

    self.screen=pygame.display.set_mode((sWidth,sHeight))
    go_fullscreen()

    self.cam = pygame.camera.Camera("/dev/video0",(sWidth,sHeight))

    self.cam.start()

    self.buttonExit = button(self.screen,
                             (self.sWidth - 200,0,200,200),
                             "images/icons/StopButton.png",
                             (0,0,0))

  def updateCamera(self):
    image = self.cam.get_image()
    self.screen.blit(image,(0,0))
    pygame.display.update()
    
  def checkExit(self, pos):
          if (self.buttonExit.checkClick(pos)):
                  self.cam.stop()
                  return True
          else:
                  return False
