import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

class vidScreen:
	def __init__(self, sWidth, sHeight, path):
		go_fullscreen()
		self.sWidth = sWidth
		self.sHeight = sHeight
                self.path = path
		self.screen = pygame.display.get_surface()
		self.screen.fill(Color(0,0,0,0), (0,0,sWidth,sHeight), 0)
                self.gameState=2
                go_fullscreen()

		self.buttonExit = button(self.screen,
		                         (self.sWidth - 200,0,200,200),
		                         "images/icons/StopButton.png",
		                         (0,0,0))

		self.re_init()

	def re_init(self):
		try:
                	self.image=pygame.image.load("%s/CAMERA1.jpg" % (self.path)).convert()
                	self.screen.blit(self.image,(0,210))
			imWidth=self.image.get_width()
			imHeight=self.image.get_height()
			try:
				self.image = pygame.image.load("%s/CAMERA2.jpg" % (self.path)).convert()
                		self.screen.blit(self.image,(self.sWidth - imWidth,self.sHeight - imHeight))
			except:
				pass
		except:
			pass

	def checkExit(self, pos):
		if (self.buttonExit.checkClick(pos)):
			return True
		else:
			return False

