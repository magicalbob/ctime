import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

class playListScreen:
	def __init__(self, sWidth, sHeight):
		go_fullscreen()
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
					"images/icons/Bob.png", 
					(0,0,0))  
		self.buttonFrozen = button(self.screen,
					(((self.sWidth * 3) / 4) - 100, 
					(self.sHeight / 2) - 100,
					200, 200),
					"images/icons/NewMusic.png", 
					(0,0,0))  

	def checkExit(self, pos):
		if (self.buttonExit.checkClick(pos)):
			return True
		else:
			return False

