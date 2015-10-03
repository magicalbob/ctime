#!/usr/bin/python
#
# Python program to entertain Christopher
#

import random
import time
import pygtk
import pygame
from pygame.locals import *
from sys import exit
from ctimeCommon import go_fullscreen
from ctimeButton import button
from ctimeGameChoose import gameChoose
from ctimeVidScreen import vidScreen
from ctimePlayList import playListScreen 
import yaml
import datetime
from time import strftime,strptime

class mainScreen:
	def __init__(self):
		self.sWidth=0
		self.sHeight=0
                pygame.init()
                self.screen=pygame.display.set_mode((self.sWidth, self.sHeight))
		screen = pygame.display.get_surface()
                self.sWidth,self.sHeight = screen.get_width(),screen.get_height()

                self.image=pygame.image.load("images/backgrounds/001.jpg").convert()
                self.tuneNo=1
                self.backNo=1
		with open('cTime.yaml','r') as confile:
			conf = yaml.load(confile)
		self.def_vol = float(conf['vol'])
                self.start_time = str(conf['start_time'])
                self.end_time = str(conf['end_time'])
                self.firstPlay=1
                self.playlist=0
                self.playLen = [ 10, 30 ]
		pygame.mixer.music.set_volume(self.def_vol)
		self.re_init()

	def re_init(self):
                self.gameState=0
                go_fullscreen()
                self.screen.blit(self.image,(0,0))
                self.playState = 1
#                self.firstPlay=1
		self.buttonPlay = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
#		self.buttonChoose = button(self.screen, (self.sWidth - 200, 0, 200, 200), "images/icons/ChooseButton.png",(255,0,0))
		self.buttonPlayList = button(self.screen, (self.sWidth - 200, 0, 200, 200), "images/icons/MusicIcon.png",(255,0,0))
		self.buttonVideo = button(self.screen, (0, self.sHeight - 200, 200, 200), "images/icons/VideoButton.png",(0,0,0))
  		
	def can_we_play(self):
		test_start = strftime('%Y-%m-%d ')+self.start_time
		test_end = strftime('%Y-%m-%d ')+self.end_time
		if test_end < test_start:
			test_end = str(datetime.datetime.strptime(test_end, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1))
		if test_start < strftime('%Y-%m-%d %H:%M:%S'):
			if strftime('%Y-%m-%d %H:%M:%S') < test_end:
				return True

		return False

	def clickButtonPlay(self):
		if not self.can_we_play():
			return
		self.playState += 1
		if self.playState > 2:
			self.playState = 1
		if self.playState == 1:
			pygame.mixer.music.pause()
			self.buttonPlay.changeImage("images/icons/PlayButton.png")
		elif self.firstPlay == 1:
                	pygame.mixer.init()
			newTune = "tunes/bob/%03d.ogg" %self.tuneNo
			pygame.mixer.music.load(newTune)
			pygame.mixer.music.play()
			self.firstPlay = 0
			self.buttonPlay.changeImage("images/icons/StopButton.png")
		else:
			pygame.mixer.music.unpause()
			self.buttonPlay.changeImage("images/icons/StopButton.png")


	def playNext(self):
		self.tuneNo += 1
		if self.tuneNo > self.playLen[self.playlist]:
			self.tuneNo = 1
                if self.playlist == 0:
		  newTune = "tunes/bob/%03d.ogg" %self.tuneNo
                else:
		  newTune = "tunes/frozen/%03d.ogg" %self.tuneNo
		pygame.mixer.music.load(newTune)
		pygame.mixer.music.play()
		 
#	def clickButtonChoose(self):
#		self.gameState = 1
#		self.firstPlay = 1
#		self.gameChoose = gameChoose(self.sWidth, self.sHeight)

	def clickButtonVideo(self):
		self.gameState = 2
		self.firstPlay = 1
#		self.playState = 1
		self.vidScreen = vidScreen(self.sWidth, self.sHeight)

        def clickPlayList(self):
                self.gameState = 3
#                self.firstPlay = 1
#               self.playState = 1
                self.playList = playListScreen(self.sWidth, self.sHeight)

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
		
#		self.clickButtonChoose()

	def checkEvent(self, event, pos):
		if event.type == pygame.MOUSEBUTTONUP:
# gameState 0: Main menu
			if self.gameState == 0:
				if (self.buttonPlay.checkClick(pos) == True):
					self.clickButtonPlay()
#				elif (self.buttonChoose.checkClick(pos) == True):
#					self.clickButtonChoose()
				elif (self.buttonVideo.checkClick(pos) == True):
					self.clickButtonVideo()
				elif (self.buttonPlayList.checkClick(pos) == True):
					self.clickPlayList()
# gameState 1: See Me Choose game
			elif self.gameState == 1:
				if self.gameChoose.checkClick(pos):
					self.playVideo()
				elif self.gameChoose.checkExit(pos):
					self.gameState = 0
					self.updatePic()

# gameState 2: Video feed from cameras
			elif self.gameState == 2:
				if self.vidScreen.checkExit(pos):
					self.gameState = 0
					self.updatePic()
#					self.re_init()

# gameState 3: play list
			elif self.gameState == 3:
				if self.playList.checkClickBob(pos):
                                        self.playlist = 0
                                        self.tuneNo = 1
			                newTune = "tunes/bob/%03d.ogg" %self.tuneNo
			                pygame.mixer.music.load(newTune)
			                pygame.mixer.music.play()
			                self.firstPlay = 0
					self.gameState = 0
					self.updatePic()
					self.re_init()
			                self.buttonPlay.changeImage("images/icons/StopButton.png")
                                        self.playState = 2
				elif self.playList.checkClickFrozen(pos):
                                        self.playlist = 1
                                        self.tuneNo = 1
			                newTune = "tunes/frozen/%03d.ogg" %self.tuneNo
			                pygame.mixer.music.load(newTune)
			                pygame.mixer.music.play()
			                self.firstPlay = 0
					self.gameState = 0
					self.updatePic()
					self.re_init()
			                self.buttonPlay.changeImage("images/icons/StopButton.png")
                                        self.playState = 2
				elif self.playList.checkExit(pos):
					self.gameState = 0
					self.updatePic()
					self.re_init()

	def updatePic(self):
		self.backNo += 1
		if self.backNo > 7:
			self.backNo = 1
		imageName = "images/backgrounds/%03d.jpg" %self.backNo
		self.image = pygame.image.load(imageName).convert()
		self.screen.blit(self.image,(0,0))
		self.buttonPlay.redraw()
		self.buttonPlayList.redraw()
		self.buttonVideo.redraw()

theGame=mainScreen()
oTime = time.time()

while True:
# Check for event. Exit if return key pressed, otherwise pass event to theGame object
	for e in pygame.event.get():
		if (e.type is KEYDOWN and e.key == K_RETURN):
			pygame.display.quit()
			exit()
		pos = pygame.mouse.get_pos()
		theGame.checkEvent(e,pos)

# Check for background picture of main screen changing
	if theGame.gameState == 0:
		nTime = time.time()
		if (nTime - oTime) > 10:
			theGame.updatePic()
			oTime = nTime

	if theGame.gameState == 2:
		theGame.vidScreen.re_init()

	if theGame.playState == 2:
		if pygame.mixer.music.get_busy() == False:
			if theGame.can_we_play():
				theGame.playNext()

	pygame.display.update()

