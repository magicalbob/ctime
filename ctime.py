#!/usr/bin/env python
""" Python program to entertain Christopher """

import random
import time
import pytz
import pygame
import pygame.locals
from ctimeCommon import go_fullscreen
from ctime_button import Button
from ctimePlayList import playListScreen
from ctimePlayList import trackListScreen
from ctimeCamera import ctimeCamera
import yaml
import datetime
from time import strftime, strptime
from ctimerSwitch import switch
from ctimePairs import pairsScreen

class mainScreen:
    def __init__(self):
        self.sWidth = 0
        self.sHeight = 0
        pygame.init()
        self.screen = pygame.display.set_mode((self.sWidth, self.sHeight))
        screen = pygame.display.get_surface()
        self.sWidth, self.sHeight = screen.get_width(), screen.get_height()

        self.image = pygame.image.load("images/backgrounds/001.jpg").convert()
        self.tuneNo = 1
        self.backNo = 1
        with open('cTime.yaml', 'r') as confile:
            conf = yaml.load(confile)
        self.def_vol = float(conf['vol'])
        self.start_time = str(conf['start_time'])
        self.end_time = str(conf['end_time'])
        self.firstPlay = 1
        self.playlist = -1
        self.playLen = [10, 32]
        self.path = str(conf['pic_loc'])
        try:
            pygame.mixer.music.set_volume(self.def_vol)
        except:
            print "pygame.music.set_volume failed"
        self.re_init()

    def re_init(self):
        self.gameState = 0
        go_fullscreen()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.sWidth-self.image.get_rect().size[0])/2),
                                      max(0, (self.sHeight-self.image.get_rect().size[1])/2)))
        self.play_state = 1
        imagePlay = ""
        imageList = ""
        if self.can_we_play():
            imagePlay = "images/icons/PlayButton.png"
            imageList = "images/icons/MusicIcon.png"
        self.button_play = Button(self.screen,
                                  (0, 0, 200, 200),
                                  imagePlay,
                                  (0, 0, 0))
        self.button_play_list = Button(self.screen,
                                       (self.sWidth - 200, 0, 200, 200),
                                       imageList,
                                       (0, 0, 0))
        self.buttonVideo = Button(self.screen,
                                  (0, self.sHeight - 200, 200, 200),
                                  "images/icons/VideoButton.png",
                                  (0, 0, 0))
        self.buttonPower = switch(self.screen,
                                  (self.sWidth - 200, self.sHeight - 200, 200, 200),
                                  "images/icons/light.png",
                                  (0, 0, 0))
        self.buttonPairs = Button(self.screen,
                                  (self.sWidth - 200, (self.sHeight / 2) - 100, 200, 200),
                                  "images/icons/pairs.png",
                                  (0, 0, 0))

    def can_we_play(self):
        uk = pytz.timezone('Europe/London')
        now_time = datetime.datetime.now(uk)
        test_start = strftime('%Y-%m-%d ')+self.start_time
        test_end = strftime('%Y-%m-%d ')+self.end_time
        s_time = datetime.datetime.strptime(test_start, "%Y-%m-%d %H:%M:%S")
        e_time = datetime.datetime.strptime(test_end, "%Y-%m-%d %H:%M:%S")
        if s_time.replace(
                tzinfo=None) < now_time.replace(
                    tzinfo=None) < e_time.replace(
                        tzinfo=None):
            return True

        return False

    def clickButtonPlay(self):
        if not self.can_we_play():
            return
        self.play_state += 1
        if self.play_state > 2:
            self.play_state = 1
        if self.play_state == 1:
            pygame.mixer.music.pause()
            self.button_play.change_image("images/icons/PlayButton.png")
        elif self.firstPlay == 1:
            try:
                pygame.mixer.init()
            except:
                print "pygame.mixer.init() failed"
            if self.playlist < 1:
                wList = "bob"
            else:
                wList = "frozen"
            newTune = "tunes/%s/%03d.ogg" % (wList, self.tuneNo)
            pygame.mixer.music.load(newTune)
            pygame.mixer.music.play()
            self.firstPlay = 0
            self.button_play.change_image("images/icons/StopButton.png")
        else:
            pygame.mixer.music.unpause()
            self.button_play.change_image("images/icons/StopButton.png")

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
        self.vidScreen = ctimeCamera(self.sWidth, self.sHeight, self.path)

    def clickPlayList(self):
        if not self.can_we_play():
            return
        self.gameState = 3
        self.play_list = playListScreen(self.sWidth, self.sHeight)

    def clickPairs(self):
        self.gameState = 5
        self.pairs = pairsScreen(self.sWidth, self.sHeight)

    def playTrack(self, play_list, tuneNo):
        whichList = ["bob", "frozen"]
        self.playlist = play_list
        self.tuneNo = tuneNo
        newTune = "tunes/%s/%03d.ogg" % (whichList[play_list], self.tuneNo)
        pygame.mixer.music.load(newTune)
        pygame.mixer.music.play()
        self.firstPlay = 0
        self.gameState = 0
        self.refreshPic()
        self.button_play.change_image("images/icons/StopButton.png")
        self.play_state = 2

    def checkEvent(self, event, pos):
        if event.type == pygame.MOUSEBUTTONUP:
            # gameState 0: Main menu
            if self.gameState == 0:
                if self.button_play.check_click(pos) == True:
                    self.clickButtonPlay()
                elif self.buttonVideo.check_click(pos) == True:
                    self.clickButtonVideo()
                elif self.button_play_list.check_click(pos) == True:
                    self.clickPlayList()
                elif self.buttonPower.check_click(pos):
                    self.refreshPic()
                elif self.buttonPairs.check_click(pos):
                    self.clickPairs()
            # gameState 2: Video feed from cameras
            elif self.gameState == 2:
                if self.vidScreen.checkExit(pos):
                    self.gameState = 0
                    self.refreshPic()

            # gameState 3: play list
            elif self.gameState == 3:
                if self.play_list.check_click_bob(pos):
                    self.gameState = 4
                    self.playlist = 0
                    self.trackList = trackListScreen(self.sWidth,
                                                     self.sHeight,
                                                     "bob",
                                                     self.playLen[0])
                elif self.play_list.check_click_frozen(pos):
                    self.gameState = 4
                    self.playlist = 1
                    self.trackList = trackListScreen(self.sWidth,
                                                     self.sHeight,
                                                     "frozen",
                                                     self.playLen[1])
                elif self.play_list.checkExit(pos):
                    self.gameState = 0
                    self.refreshPic()

            # gameState 4: track list
            elif self.gameState == 4:
                trackNo, isClicked = self.trackList.check_click(pos)
                if isClicked == True:
                    if (self.playlist == 1) and (trackNo == 5):
                        self.clickPairs()
                    else:
                        self.playTrack(self.playlist, trackNo)
            # gameState 5: Pairs game
            elif self.gameState == 5:
                pairState, isClicked = self.pairs.check_click(pos)
                if pairState == -2:
                    self.gameState = 0
                    self.refreshPic()

    def refreshPic(self):
        imageName = "images/backgrounds/%03d.jpg" %self.backNo
        self.image = pygame.image.load(imageName).convert()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.sWidth-self.image.get_rect().size[0])/2),
                                      max(0, (self.sHeight-self.image.get_rect().size[1])/2)))
        self.button_play.redraw()
        self.button_play_list.redraw()
        self.buttonVideo.redraw()
        if self.buttonPower.enabled == True:
            self.buttonPower.redraw()
        self.buttonPairs.redraw()

    def updatePic(self):
        self.backNo += 1
        if self.backNo > 7:
            self.backNo = 1
        self.refreshPic()

theGame = mainScreen()
oTime = time.time()

while True:
    # Check power off of lights
    theGame.buttonPower.checkOff()
    # Check for event. Exit if return key pressed, otherwise pass event to theGame object
    for e in pygame.event.get():
        if (e.type is pygame.KEYDOWN and e.key == pygame.K_RETURN):
            pygame.display.quit()
            exit()
        pos = pygame.mouse.get_pos()
        theGame.checkEvent(e, pos)

    # Check for background picture of main screen changing
    if theGame.gameState == 0:
        nTime = time.time()
        if (nTime - oTime) > 10:
            theGame.updatePic()
            oTime = nTime
        if theGame.buttonPower.checkButton() == True:
            theGame.refreshPic()

    if theGame.play_state == 2:
        if pygame.mixer.music.get_busy() == False:
            if theGame.can_we_play():
                theGame.playNext()

    if theGame.gameState == 5:
        theGame.pairs.flipBack()

    if theGame.gameState == 2:
        theGame.vidScreen.updateCamera()

    pygame.display.update()
