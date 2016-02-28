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
from ctimePlayList import trackListScreen 
import yaml
import datetime
from time import strftime,strptime
from ctimerSwitch import switch
from ctimePairs import pairsScreen

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
                self.playlist=-1
                self.playLen = [ 10, 32 ]
                self.path = str(conf['pic_loc'])
                try:
		  pygame.mixer.music.set_volume(self.def_vol)
                except:
                  print "pygame.music.set_volume failed"
		self.re_init()

	def re_init(self):
                self.gameState=0
                go_fullscreen()
                self.screen.blit(self.image,(0,0))
                self.playState = 1
		self.buttonPlay = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
		self.buttonPlayList = button(self.screen, (self.sWidth - 200, 0, 200, 200), "images/icons/MusicIcon.png",(0,0,0))
		self.buttonVideo = button(self.screen, (0, self.sHeight - 200, 200, 200), "images/icons/VideoButton.png",(0,0,0))
		self.buttonPower = switch(self.screen, (self.sWidth - 200, self.sHeight - 200, 200, 200), "images/icons/light.png",(0,0,0))
		self.buttonPairs = button(self.screen, (self.sWidth - 200, (self.sHeight / 2) - 100, 200, 200), "images/icons/pairs.png",(0,0,0))
  		
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
                        try:
                	  pygame.mixer.init()
                        except:
                          print "pygame.mixer.init() failed"
			newTune = "tunes/bob/%03d.ogg" %self.tuneNo
			pygame.mixer.music.load(newTune)
			pygame.mixer.music.play()
			self.firstPlay = 0
			self.buttonPlay.changeImage("images/icons/StopButton.png")
		else:
			pygame.mixer.music.unpause()
			self.buttonPlay.changeImage("images/icons/StopButton.png")


	def playNext(self):
                if not self.can_we_play():
                        return
		self.tuneNo += 1
		if self.tuneNo > self.playLen[self.playlist]:
			self.tuneNo = 1
                if self.playlist == 0:
		  newTune = "tunes/bob/%03d.ogg" %self.tuneNo
                else:
		  newTune = "tunes/frozen/%03d.ogg" %self.tuneNo
		pygame.mixer.music.load(newTune)
		pygame.mixer.music.play()
		 
	def clickButtonVideo(self):
		self.gameState = 2
		self.firstPlay = 1
		self.vidScreen = vidScreen(self.sWidth, self.sHeight, self.path)

        def clickPlayList(self):
                self.gameState = 3
                self.playList = playListScreen(self.sWidth, self.sHeight)

        def clickPairs(self):
                self.gameState = 5
                self.pairs = pairsScreen(self.sWidth, self.sHeight)

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

        def playTrack(self,playList, tuneNo):
          whichList = [ "bob", "frozen" ]
          self.playlist = playList 
          self.tuneNo = tuneNo
          newTune = "tunes/%s/%03d.ogg" % (whichList[playList],self.tuneNo)
          pygame.mixer.music.load(newTune)
          pygame.mixer.music.play()
          self.firstPlay = 0
          self.gameState = 0
          self.refreshPic()
          self.buttonPlay.changeImage("images/icons/StopButton.png")
          self.playState = 2
		
	def checkEvent(self, event, pos):
		if event.type == pygame.MOUSEBUTTONUP:
# gameState 0: Main menu
			if self.gameState == 0:
				if (self.buttonPlay.checkClick(pos) == True):
					self.clickButtonPlay()
				elif (self.buttonVideo.checkClick(pos) == True):
					self.clickButtonVideo()
				elif (self.buttonPlayList.checkClick(pos) == True):
					self.clickPlayList()
                                elif (self.buttonPower.checkClick(pos)):
                                        self.refreshPic()
                                elif (self.buttonPairs.checkClick(pos)):
                                        self.clickPairs()
# gameState 1: See Me Choose game
			elif self.gameState == 1:
				if self.gameChoose.checkClick(pos):
					self.playVideo()
				elif self.gameChoose.checkExit(pos):
					self.gameState = 0
					self.refreshPic()

# gameState 2: Video feed from cameras
			elif self.gameState == 2:
				if self.vidScreen.checkExit(pos):
					self.gameState = 0
					self.refreshPic()

# gameState 3: play list
			elif self.gameState == 3:
				if self.playList.checkClickBob(pos):
                                  if self.playlist == -1:
                                    self.playTrack(0,1)
                                  else:
                                        self.gameState = 4
                                        self.playlist = 0
                                        self.trackList = trackListScreen(self.sWidth,
                                                                         self.sHeight,
                                                                         "bob",
                                                                         self.playLen[0])
				elif self.playList.checkClickFrozen(pos):
                                  if self.playlist == -1:
                                    self.playTrack(1,1)
                                  else:
                                        self.gameState = 4
                                        self.playlist = 1
                                        self.trackList = trackListScreen(self.sWidth,
                                                                         self.sHeight,
                                                                         "frozen",
                                                                         self.playLen[1])
				elif self.playList.checkExit(pos):
					self.gameState = 0
					self.refreshPic()

# gameState 4: track list
			elif self.gameState == 4:
				trackNo, isClicked = self.trackList.checkClick(pos)
                                if isClicked == True:
                                    self.playTrack(self.playlist, trackNo)
# gameState 5: Pairs game
			elif self.gameState == 5:
                                pairState, isClicked = self.pairs.checkClick(pos)
                                if pairState == -2:
                                    self.gameState = 0
                                    self.refreshPic()

        def refreshPic(self):
		imageName = "images/backgrounds/%03d.jpg" %self.backNo
		self.image = pygame.image.load(imageName).convert()
		self.screen.blit(self.image,(0,0))
		self.buttonPlay.redraw()
		self.buttonPlayList.redraw()
		self.buttonVideo.redraw()
                if self.buttonPower.enabled == True:
		  self.buttonPower.redraw()
                self.buttonPairs.redraw()

	def updatePic(self):
		self.backNo += 1
		if self.backNo > 7:
			self.backNo = 1
                self.refreshPic()

theGame=mainScreen()
oTime = time.time()

while True:
# Check power off of lights
        theGame.buttonPower.checkOff()
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
                if theGame.buttonPower.checkButton() == True:
                  theGame.refreshPic()

	if theGame.gameState == 2:
		theGame.vidScreen.re_init()

	if theGame.playState == 2:
		if pygame.mixer.music.get_busy() == False:
			if theGame.can_we_play():
				theGame.playNext()

        if theGame.gameState == 5:
                theGame.pairs.flipBack()

	pygame.display.update()

