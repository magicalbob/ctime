import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeCommon import shuffleList
from ctime_button import Button
import random

class trackListScreen:
  def __init__(self, sWidth, sHeight, playList, tracks):
    self.sWidth = sWidth
    self.sHeight = sHeight
    self.screen = pygame.display.get_surface()
    self.screen.fill(Color(0,0,0,0), (0,0,sWidth,sHeight), 0)
    self.gameState=4
    go_fullscreen()

    self.playList = playList
    self.tracks = tracks
    self.trackList = []

    self.trackRandom = []
    for tIdx in range(0,self.tracks):
      self.trackRandom.append(self.getButtonPos(tIdx))
    self.trackRandom=shuffleList(self.trackRandom)

    trackIdx = 0
    while trackIdx < self.tracks:
      xPos, yPos = self.trackRandom[trackIdx]
      self.trackList.append(
        Button(self.screen,
               (xPos,yPos,150,150),
               "images/icons/%s/%03d.png" % (playList, trackIdx+1),
               (0,0,0))
      )
      trackIdx += 1
         
  def getButtonPos(self, buttonNo):
    bCol = buttonNo % 8
    bRow = buttonNo / 8

    padX = (self.sWidth - 1200) / 9
    padY = (self.sHeight - 600) / 5    

    return [ padX + (bCol * (150 + padX)), padY + (bRow * (150 + padY)) ]

  def check_click(self, pos):
    trackIdx = 0
    while trackIdx < self.tracks:
      if self.trackList[trackIdx].check_click(pos):
        return [ trackIdx + 1, True ]
      trackIdx += 1
    return [ -1, False ]

class playListScreen:
  def __init__(self, sWidth, sHeight):
    self.sWidth = sWidth
    self.sHeight = sHeight
    self.screen = pygame.display.get_surface()
    self.screen.fill(Color(0,0,0,0), (0,0,sWidth,sHeight), 0)
    self.gameState=3
    go_fullscreen()

    buttonPosition=[]
    buttonPosition.append(
                          (
                           (self.sWidth / 4) - 100, 
                           (self.sHeight / 2) - 100,
                           200, 
                           200
                          )
                         )
    buttonPosition.append(
                          (
                           ((self.sWidth * 3) / 4) - 100, 
                           (self.sHeight / 2) - 100,
                           200,
                           200
                          )
                         )


    button1st=random.randint(0,1)
    button2nd=1-button1st

    self.buttonExit = Button(self.screen,
                             (self.sWidth - 200,0,200,200),
                             "images/icons/StopButton.png",
                             (0,0,0))

    self.buttonBob = Button(self.screen,
                            buttonPosition[button1st],
                            "images/icons/bob.png", 
                            (0,0,0))  

    self.buttonFrozen = Button(self.screen,
                               buttonPosition[button2nd],
                               "images/icons/frozen.png", 
                               (0,0,0))  

  def check_click_bob(self, pos):
    if (self.buttonBob.check_click(pos)):
      return True
    else:
      return False

  def check_click_frozen(self, pos):
    if (self.buttonFrozen.check_click(pos)):
      return True
    else:
      return False

  def checkExit(self, pos):
    if (self.buttonExit.check_click(pos)):
      return True
    else:
      return False

