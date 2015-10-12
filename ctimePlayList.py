import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

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

    trackIdx = 0
    while trackIdx < self.tracks:
      xPos, yPos = self.getButtonPos(trackIdx)
      self.trackList.append(
        button(self.screen,
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

  def checkClick(self, pos):
    trackIdx = 0
    while trackIdx < self.tracks:
      if self.trackList[trackIdx].checkClick(pos):
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

		self.buttonExit = button(self.screen,
		                         (self.sWidth - 200,0,200,200),
		                         "images/icons/StopButton.png",
		                         (0,0,0))

		self.buttonBob = button(self.screen,
					((self.sWidth / 4) - 100, 
					(self.sHeight / 2) - 100,
					200, 200),
					"images/icons/bob.png", 
					(0,0,0))  
		self.buttonFrozen = button(self.screen,
					(((self.sWidth * 3) / 4) - 100, 
					(self.sHeight / 2) - 100,
					200, 200),
					"images/icons/frozen.png", 
					(0,0,0))  

	def checkClickBob(self, pos):
                if (self.buttonBob.checkClick(pos)):
                        return True
                else:
                        return False

	def checkClickFrozen(self, pos):
		if (self.buttonFrozen.checkClick(pos)):
			return True
                else:
                        return False

	def checkExit(self, pos):
		if (self.buttonExit.checkClick(pos)):
			return True
		else:
			return False

