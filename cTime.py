#!/usr/bin/python
#
# Python program to entertain Christopher
#

import random
import time
import gtk
import pygtk
import pygame
from pygame.locals import *
from sys import exit

def go_fullscreen():
	screen = pygame.display.get_surface()
	tmp = screen.convert()
	caption = pygame.display.get_caption()
	cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
	w,h = screen.get_width(),screen.get_height()
	flags = screen.get_flags()
	bits = screen.get_bitsize()
	
	pygame.display.init()
	
	screen = pygame.display.set_mode((w,h),flags|FULLSCREEN,bits)
	screen.blit(tmp,(0,0))
	pygame.display.set_caption(*caption)
 
	pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
	pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
	
	return screen

class button:
	def __init__(self, screen, rect, image, colorkey):
		self.rect=rect
		self.colorkey=colorkey
		self.image=pygame.image.load(image).convert()
		self.image.set_colorkey(colorkey)
		self.screen=screen
		self.screen.blit(self.image,(self.rect[0], self.rect[1]))
		self.oTime = time.time()

	def redraw(self):
		self.screen.blit(self.image,(self.rect[0], self.rect[1]))

	def changeImage(self, image):
		self.image=pygame.image.load(image).convert()
		self.image.set_colorkey(self.colorkey)
		self.screen.blit(self.image, (self.rect[0], self.rect[1]))

	def checkClick(self, pos):
		retVal = False

		nTime = time.time()
		if (nTime - self.oTime) > 1:
			self.oTime = nTime
			if ((pos[0] >= self.rect[0]) and
			    (pos[0] <= self.rect[0] + self.rect[2])):
				if ((pos[1] >= self.rect[1]) and
				    (pos[1] <= self.rect[1] + self.rect[3])):
					retVal = True
		return retVal

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

class mainScreen:
	def __init__(self):
                self.sWidth=gtk.gdk.screen_width()
		self.sHeight=gtk.gdk.screen_height()
                pygame.init()
                self.screen=pygame.display.set_mode((self.sWidth, self.sHeight))
		screen = pygame.display.get_surface()
                self.sWidth,self.sHeight = screen.get_width(),screen.get_height()

                self.image=pygame.image.load("images/backgrounds/001.jpg").convert()
                self.tuneNo=1
                self.backNo=1
		self.re_init()

	def re_init(self):
                self.gameState=0
                go_fullscreen()
                self.screen.blit(self.image,(0,0))
                self.playState = 1
                self.firstPlay=1
		self.buttonPlay = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
		self.buttonChoose = button(self.screen, (self.sWidth - 200, 0, 200, 200), "images/icons/ChooseButton.png",(255,0,0))
		self.buttonVideo = button(self.screen, (0, self.sHeight - 200, 200, 200), "images/icons/VideoButton.png",(0,0,0))

	def clickButtonPlay(self):
		self.playState += 1
		if self.playState > 2:
			self.playState = 1
		if self.playState == 1:
			pygame.mixer.music.pause()
			self.buttonPlay.changeImage("images/icons/PlayButton.png")
		elif self.firstPlay == 1:
                	pygame.mixer.init()
			newTune = "tunes/%03d.ogg" %self.tuneNo
			pygame.mixer.music.load(newTune)
			pygame.mixer.music.play()
			self.firstPlay = 0
			self.buttonPlay.changeImage("images/icons/StopButton.png")
		else:
			pygame.mixer.music.unpause()
			self.buttonPlay.changeImage("images/icons/StopButton.png")

	def playNext(self):
		self.tuneNo += 1
		if self.tuneNo > 10:
			self.tuneNo = 1
		newTune = "tunes/%03d.ogg" %self.tuneNo
		pygame.mixer.music.load(newTune)
		pygame.mixer.music.play()
		 

	def clickButtonChoose(self):
		self.gameState = 1
		self.firstPlay = 1
		self.playState = 1
		self.gameChoose = gameChoose(self.sWidth, self.sHeight)

	def playVideo(self):
		FPS = 25

		pygame.mixer.quit()
		clock = pygame.time.Clock()
		movieName = "videos/%03d.MPG" %random.randint(1,3)
		print "movieName = " + movieName
		movie = pygame.movie.Movie(movieName)
		screen = pygame.display.set_mode(movie.get_size())
		movie_screen = pygame.Surface(movie.get_size()).convert()

		movie.set_display(movie_screen)
		go_fullscreen()
		movie.set_volume(1)
		movie.play()
		playing = True
		while movie.get_busy():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					movie.stop()
					playing = False
			try:
				screen.blit(movie_screen,(0,0))
			except:
				pass
			pygame.display.update()
			clock.tick(FPS)
		pygame.display.set_mode((self.sWidth, self.sHeight))
		
		self.clickButtonChoose()

	def checkEvent(self, event, pos):
		if event.type == pygame.MOUSEBUTTONUP:
			if self.gameState == 0:
				if (self.buttonPlay.checkClick(pos) == True):
					self.clickButtonPlay()
				elif (self.buttonChoose.checkClick(pos) == True):
					self.clickButtonChoose()
				elif (self.buttonVideo.checkClick(pos) == True):
					self.clickButtonChoose()
			elif self.gameState == 1:
				if self.gameChoose.checkClick(pos):
					self.playVideo()
				elif self.gameChoose.checkExit(pos):
					self.re_init()

	def updatePic(self):
		self.backNo += 1
		if self.backNo > 7:
			self.backNo = 1
		imageName = "images/backgrounds/%03d.jpg" %self.backNo
		self.image = pygame.image.load(imageName).convert()
		self.screen.blit(self.image,(0,0))
		self.buttonPlay.redraw()
		self.buttonChoose.redraw()
		self.buttonVideo.redraw()

theGame=mainScreen()
oTime = time.time()

while True:
	for e in pygame.event.get():
		if (e.type is KEYDOWN and e.key == K_RETURN):
			pygame.display.quit()
			exit()
		pos = pygame.mouse.get_pos()
		theGame.checkEvent(e,pos)

	if theGame.gameState == 0:
		nTime = time.time()
		if (nTime - oTime) > 10:
			theGame.updatePic()
			oTime = nTime

	if theGame.playState == 2:
		if pygame.mixer.music.get_busy() == False:
			theGame.playNext()

	pygame.display.update()

