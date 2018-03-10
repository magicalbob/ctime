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

class MainScreen:
    def __init__(self):
        self.sWidth = 0
        self.sHeight = 0
        pygame.init()
        self.screen = pygame.display.set_mode((self.sWidth, self.sHeight))
        screen = pygame.display.get_surface()
        self.sWidth, self.sHeight = screen.get_width(), screen.get_height()

        self.image = pygame.image.load("images/backgrounds/001.jpg").convert()
        self.game_state = 0
        self.tune_no = 1
        self.back_no = 1
        with open('cTime.yaml', 'r') as confile:
            conf = yaml.load(confile)
        self.def_vol = float(conf['vol'])
        self.start_time = str(conf['start_time'])
        self.end_time = str(conf['end_time'])
        self.first_play = 1
        self.playlist = -1
        self.play_len = [10, 32]
        self.path = str(conf['pic_loc'])
        try:
            pygame.mixer.music.set_volume(self.def_vol)
        except:
            print "pygame.music.set_volume failed"
        self.re_init()

    def re_init(self):
        self.game_state = 0
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
        self.button_video = Button(self.screen,
                                   (0, self.sHeight - 200, 200, 200),
                                   "images/icons/VideoButton.png",
                                   (0, 0, 0))
        self.button_power = switch(self.screen,
                                   (self.sWidth - 200, self.sHeight - 200, 200, 200),
                                   "images/icons/light.png",
                                   (0, 0, 0))
        self.button_pairs = Button(self.screen,
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
        elif self.first_play == 1:
            try:
                pygame.mixer.init()
            except:
                print "pygame.mixer.init() failed"
            if self.playlist < 1:
                wList = "bob"
            else:
                wList = "frozen"
            new_tune = "tunes/%s/%03d.ogg" % (wList, self.tune_no)
            pygame.mixer.music.load(new_tune)
            pygame.mixer.music.play()
            self.first_play = 0
            self.button_play.change_image("images/icons/StopButton.png")
        else:
            pygame.mixer.music.unpause()
            self.button_play.change_image("images/icons/StopButton.png")

    def playNext(self):
        if not self.can_we_play():
            return
        self.tune_no += 1
        if self.tune_no > self.play_len[self.playlist]:
            self.tune_no = 1
        if self.playlist == 0:
            new_tune = "tunes/bob/%03d.ogg" %self.tune_no
        else:
            new_tune = "tunes/frozen/%03d.ogg" %self.tune_no
        pygame.mixer.music.load(new_tune)
        pygame.mixer.music.play()

    def clickButtonVideo(self):
        self.game_state = 2
        self.first_play = 1
        self.vidScreen = ctimeCamera(self.sWidth, self.sHeight, self.path)

    def clickPlayList(self):
        if not self.can_we_play():
            return
        self.game_state = 3
        self.play_list = playListScreen(self.sWidth, self.sHeight)

    def clickPairs(self):
        self.game_state = 5
        self.pairs = pairsScreen(self.sWidth, self.sHeight)

    def playTrack(self, play_list, tune_no):
        whichList = ["bob", "frozen"]
        self.playlist = play_list
        self.tune_no = tune_no
        new_tune = "tunes/%s/%03d.ogg" % (whichList[play_list], self.tune_no)
        pygame.mixer.music.load(new_tune)
        pygame.mixer.music.play()
        self.first_play = 0
        self.game_state = 0
        self.refreshPic()
        self.button_play.change_image("images/icons/StopButton.png")
        self.play_state = 2

    def checkEvent(self, event, pos):
        if event.type == pygame.MOUSEBUTTONUP:
            # game_state 0: Main menu
            if self.game_state == 0:
                if self.button_play.check_click(pos) == True:
                    self.clickButtonPlay()
                elif self.button_video.check_click(pos) == True:
                    self.clickButtonVideo()
                elif self.button_play_list.check_click(pos) == True:
                    self.clickPlayList()
                elif self.button_power.check_click(pos):
                    self.refreshPic()
                elif self.button_pairs.check_click(pos):
                    self.clickPairs()
            # game_state 2: Video feed from cameras
            elif self.game_state == 2:
                if self.vidScreen.checkExit(pos):
                    self.game_state = 0
                    self.refreshPic()

            # game_state 3: play list
            elif self.game_state == 3:
                if self.play_list.check_click_bob(pos):
                    self.game_state = 4
                    self.playlist = 0
                    self.track_list = trackListScreen(self.sWidth,
                                                      self.sHeight,
                                                      "bob",
                                                      self.play_len[0])
                elif self.play_list.check_click_frozen(pos):
                    self.game_state = 4
                    self.playlist = 1
                    self.track_list = trackListScreen(self.sWidth,
                                                      self.sHeight,
                                                      "frozen",
                                                      self.play_len[1])
                elif self.play_list.checkExit(pos):
                    self.game_state = 0
                    self.refreshPic()

            # game_state 4: track list
            elif self.game_state == 4:
                trackNo, isClicked = self.track_list.check_click(pos)
                if isClicked == True:
                    if (self.playlist == 1) and (trackNo == 5):
                        self.clickPairs()
                    else:
                        self.playTrack(self.playlist, trackNo)
            # game_state 5: Pairs game
            elif self.game_state == 5:
                pairState, isClicked = self.pairs.check_click(pos)
                if pairState == -2:
                    self.game_state = 0
                    self.refreshPic()

    def refreshPic(self):
        imageName = "images/backgrounds/%03d.jpg" %self.back_no
        self.image = pygame.image.load(imageName).convert()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.sWidth-self.image.get_rect().size[0])/2),
                                      max(0, (self.sHeight-self.image.get_rect().size[1])/2)))
        self.button_play.redraw()
        self.button_play_list.redraw()
        self.button_video.redraw()
        if self.button_power.enabled == True:
            self.button_power.redraw()
        self.button_pairs.redraw()

    def updatePic(self):
        self.back_no += 1
        if self.back_no > 7:
            self.back_no = 1
        self.refreshPic()

theGame = MainScreen()
oTime = time.time()

while True:
    # Check power off of lights
    theGame.button_power.checkOff()
    # Check for event. Exit if return key pressed, otherwise pass event to theGame object
    for e in pygame.event.get():
        if (e.type is pygame.KEYDOWN and e.key == pygame.K_RETURN):
            pygame.display.quit()
            exit()
        pos = pygame.mouse.get_pos()
        theGame.checkEvent(e, pos)

    # Check for background picture of main screen changing
    if theGame.game_state == 0:
        nTime = time.time()
        if (nTime - oTime) > 10:
            theGame.updatePic()
            oTime = nTime
        if theGame.button_power.checkButton() == True:
            theGame.refreshPic()

    if theGame.play_state == 2:
        if pygame.mixer.music.get_busy() == False:
            if theGame.can_we_play():
                theGame.playNext()

    if theGame.game_state == 5:
        theGame.pairs.flipBack()

    if theGame.game_state == 2:
        theGame.vidScreen.updateCamera()

    pygame.display.update()
