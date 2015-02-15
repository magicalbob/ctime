import random
import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeButton import button

class gameChoose:
	def __init__(self, sWidth, sHeight):
		go_fullscreen()
		w = sWidth
		h = sHeight
		screen = pygame.display.get_surface()
		screen.fill(Color(255,0,0,0), (0,0,w,h/2), 0)
		screen.fill(Color(0,255,0,0), (0,h/2,w,h/2), 0)
		imageCat = random.randint(1,4)
		imageNum = [random.randint(1,20),
		            random.randint(1,20),
		            random.randint(1,20),
		            random.randint(1,20)]
		while imageNum[1] == imageNum[0]:
			imageNum[1] = random.randint(1,20)
		while ((imageNum[2] == imageNum[0]) or
		       (imageNum[2] == imageNum[1])):
			imageNum[2] = random.randint(1,20)
		while ((imageNum[3] == imageNum[0]) or
		       (imageNum[3] == imageNum[1]) or
		       (imageNum[3] == imageNum[2])):
			imageNum[3] = random.randint(1,20)

		imageName=["images/seemechoose/%1d%02d.jpg" %(imageCat, imageNum[0]),"images/seemechoose/%1d%02d.jpg" %(imageCat, imageNum[1]),"images/seemechoose/%1d%02d.jpg" %(imageCat, imageNum[2]),"images/seemechoose/%1d%02d.jpg" %(imageCat, imageNum[3])]
		self.buttons = [button(screen,
		                      ((w/5)-100,((3 * h) / 4)-100,200,200),
		                      imageName[0],
		                      (0,0,0)),
		                button(screen,
		                      ((2*(w/5))-100,((3 * h) / 4)-100,200,200),
		                      imageName[1],
		                      (0,0,0)),
		                button(screen,
		                      ((3*(w/5))-100,((3 * h) / 4)-100,200,200),
		                      imageName[2],
		                      (0,0,0)),
		                button(screen,
		                      ((4*(w/5))-100,((3 * h) / 4)-100,200,200),
		                      imageName[3],
		                      (0,0,0))]
		self.correctImageNo = random.randint(1,4) - 1
		screen.blit(self.buttons[self.correctImageNo].image,
		            ((w/2) -100,
		             ((h/4) -100)))
		self.buttonExit = button(screen,
		                         (w - 200,0,200,200),
		                         "images/icons/StopButton.png",
		                         (0,0,0))

	def checkClick(self, pos):
		if (self.buttons[self.correctImageNo].checkClick(pos)):
			return True
		else:
			return False

	def checkExit(self, pos):
		if (self.buttonExit.checkClick(pos)):
			return True
		else:
			return False


