#!/usr/bin/env python
""" Python program to entertain Christopher """

import time
from time import strftime
import datetime
from datetime import timedelta
import pytz
import pygame
import pygame.locals
import yaml
import os
import logging
from ctime_common import go_fullscreen
from ctime_button import Button
from ctime_play_list import PlayListScreen
from ctime_play_list import TrackListScreen
from ctime_camera import Camera
from ctime_switch import Switch
from ctime_pairs import PairsScreen
from ctime_skype import CtimeSkype

class MainScreen(object):
    """ The main screen of the program """
    def __init__(self):
        logging.basicConfig(filename='ctime.log',level=logging.INFO)
        logging.info('started up')
        self.screen_width = 0
        self.screen_height = 0
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

        self.image = pygame.image.load("images/backgrounds/001.jpg").convert()
        self.game_state = 0
        self.play_state = 1
        self.tune_no = 1
        self.back_no = 1
        with open('cTime.yaml', 'r') as confile:
            conf = yaml.load(confile)
        self.def_vol = float(conf['vol'])
        self.start_time = str(conf['start_time'])
        self.end_time = str(conf['end_time'])
        self.max_play_length = conf['max_play_length']
        try:
            self.power_on = conf['power_on']
        except:
            self.power_on = ''
        try:
            self.power_off = conf['power_off']
        except:
            self.power_off = ''
        try:
          self.skype_user = conf['skype_user']
        except:
          self.skype_user = None
        try:
          self.skype_pass = conf['skype_pass']
        except:
          self.skype_pass = None
        try:
          self.skype_start = conf['skype_start']
        except:
          self.skype_start = None
        try:
          self.skype_end = conf['skype_end']
        except:
          self.skype_end = None
        try:
          self.skype_timeout = conf['skype_timeout']
        except:
          self.skype_timeout = None
        self.skype_exit = None
        self.play_start = datetime.datetime.now(pytz.timezone('Europe/London')) 
        self.first_play = 1
        self.playlist = -1
        self.play_len = [10, 32, 11]
        self.path = str(conf['pic_loc'])
        self.video_screen = None
        self.play_list = None
        self.track_list = None
        self.pairs = None
        try:
            pygame.mixer.music.set_volume(self.def_vol)
        except:
            logging.error('pygame.music.set_volume failed')
        self.re_init()

    def re_init(self):
        """ re-initialise the screen - used when sub screen closes """
        self.game_state = 0
        go_fullscreen()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.screen_width-self.image.get_rect().size[0])/2),
                                      max(0, (self.screen_height-self.image.get_rect().size[1])/2)))
        self.play_state = 1
        image_play = ""
        image_list = ""
        if self.can_we_play():
            image_play = "images/icons/PlayButton.png"
            image_list = "images/icons/MusicIcon.png"
        self.button_play = Button(self.screen,
                                  (0, 0, 200, 200),
                                  image_play,
                                  (0, 0, 0))
        self.button_play_list = Button(self.screen,
                                       (self.screen_width - 200, 0, 200, 200),
                                       image_list,
                                       (0, 0, 0))
        if os.path.exists("/dev/video0"):
            self.button_video = Button(self.screen,
                                       (0, self.screen_height - 200, 200, 200),
                                       "images/icons/VideoButton.png",
                                       (0, 0, 0))
        else:
            self.button_video = None
        self.button_power = Switch(self.screen,
                                   (self.screen_width - 200, self.screen_height - 200, 200, 200),
                                   "images/icons/light.png",
                                   (0, 0, 0),
                                   self.power_on,
                                   self.power_off)
        self.button_pairs = Button(self.screen,
                                   (self.screen_width - 200,
                                    (self.screen_height / 2) - 100,
                                    200,
                                    200),
                                   "images/icons/pairs.png",
                                   (0, 0, 0))
        if self.can_we_skype():
            self.button_skype = Button(self.screen,
                                       (0,
                                        (self.screen_height / 2) - 100,
                                        200,
                                        200),
                                       "images/icons/Phone.png",
                                       (0, 0, 0))
        else:
            self.button_skype = None

    def can_we_skype(self):
        """ check config settings available """
        if (not os.path.exists("/dev/video0") or
            self.skype_user  == None or 
            self.skype_pass  == None or
            self.skype_start == None or
            self.skype_end   == None):
           """ not according to config """
           return False

        """ check the time. if too late say no """
        now_time = datetime.datetime.now(pytz.timezone('Europe/London'))
        test_start = strftime('%Y-%m-%d ')+self.skype_start
        test_end   = strftime('%Y-%m-%d ')+self.skype_end
        s_time = datetime.datetime.strptime(test_start, "%Y-%m-%d %H:%M:%S")
        e_time = datetime.datetime.strptime(test_end, "%Y-%m-%d %H:%M:%S")
        if s_time.replace(
                tzinfo=None) < now_time.replace(
                    tzinfo=None) < e_time.replace(
                        tzinfo=None):
            pass
        else:
            return False

        """ check that skype hasn't been used to recently """
        if self.skype_timeout == None:
            return True

        if self.skype_exit == None:
            return True

        if time.time() - self.skype_exit > self.skype_timeout:
            return True

        return False

    def can_we_play(self):
        """ check the time. if too late say no """
        now_time = datetime.datetime.now(pytz.timezone('Europe/London'))
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

    def click_button_play(self):
        """ if play pressed, check time, then check if play list already selected """
        if not self.can_we_play():
            return
        """ add 1 to play_state. If greater than 2 put it back to 1. 1 means "not playing", 2 means "playing" """
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
                logging.error('pygame.mixer.init() failed')
            if self.playlist < 1:
                which_list = "bob"
            elif self.playlist == 1:
                which_list = "frozen"
            else:
                which_list = "showman"
            new_tune = "tunes/%s/%03d.ogg" % (which_list, self.tune_no)
            pygame.mixer.music.load(new_tune)
            pygame.mixer.music.play()
            self.first_play = 0
            self.button_play.change_image("images/icons/StopButton.png")
            self.play_start = datetime.datetime.now(pytz.timezone('Europe/London')) 
        else:
            pygame.mixer.music.unpause()
            self.button_play.change_image("images/icons/StopButton.png")
            self.play_start = datetime.datetime.now(pytz.timezone('Europe/London')) 

    def play_next(self):
        """ when track finishes check to see what next one is (or not if too late) """
        if not self.can_we_play():
            return
        """ have we been playing too long """
        now_time = datetime.datetime.now(pytz.timezone('Europe/London'))
        if now_time - self.play_start > timedelta(minutes=self.max_play_length):
            self.play_state = 1
            if self.game_state == 0:
                self.button_play.change_image("images/icons/PlayButton.png")
            return
        self.tune_no += 1
        if self.tune_no > self.play_len[self.playlist]:
            self.tune_no = 1
        if self.playlist == 0:
            new_tune = "tunes/bob/%03d.ogg" %self.tune_no
        elif self.playlist == 1:
            new_tune = "tunes/frozen/%03d.ogg" %self.tune_no
        else:
            new_tune = "tunes/showman/%03d.ogg" %self.tune_no
        pygame.mixer.music.load(new_tune)
        pygame.mixer.music.play()

    def click_button_video(self):
        """ start video show """
        logging.info('start video show')
        self.game_state = 2
        self.first_play = 1
        self.video_screen = Camera(self.screen_width, self.screen_height, self.path)

    def click_play_list(self):
        """ display play list selection (if not too late) """
        logging.info('display play list selection (if not too late)')
        if not self.can_we_play():
            return
        self.game_state = 3
        self.play_list = PlayListScreen(self.screen_width, self.screen_height)

    def click_pairs(self):
        """ start pairs game """
        logging.info('start pairs game')
        self.game_state = 5
        self.pairs = PairsScreen(self.screen_width, self.screen_height)

    def click_skype(self):
        """ start skype chat """
        logging.info('start skype chat')
        self.game_state = 6
        self.skype = CtimeSkype(self, self.skype_user, self.skype_pass)

    def play_track(self, play_list, tune_no):
        """ play some music """
        logging.info('play some music')
        which_list = ["bob", "frozen", "showman"]
        self.playlist = play_list
        self.tune_no = tune_no
        new_tune = "tunes/%s/%03d.ogg" % (which_list[play_list], self.tune_no)
        pygame.mixer.music.load(new_tune)
        pygame.mixer.music.play()
        self.first_play = 0
        self.game_state = 0
        self.refresh_pic()
        self.button_play.change_image("images/icons/StopButton.png")
        self.play_state = 2

    def check_event(self, event, coord):
        """ check event and decide how to react """
        if event.type == pygame.MOUSEBUTTONUP:
            # game_state 0: Main menu
            if self.game_state == 0:
                if self.button_play.check_click(coord):
                    logging.info('button_play clicked')
                    self.click_button_play()
                elif (self.button_video != None and
                      self.button_video.check_click(coord)):
                    logging.info('button_video clicked')
                    self.click_button_video()
                elif self.button_play_list.check_click(coord):
                    logging.info('button_play_list clicked')
                    self.click_play_list()
                elif self.button_power.check_click(coord):
                    logging.info('button_power clicked')
                    self.refresh_pic()
                elif self.button_pairs.check_click(coord):
                    logging.info('button_pairs clicked')
                    self.click_pairs()
                elif self.button_skype != None:
                    if self.button_skype.check_click(coord):
                        logging.info('button_skype clicked')
                        self.button_skype = None
                        self.click_skype()
            # game_state 2: Video feed from cameras
            elif self.game_state == 2:
                if self.video_screen.check_exit(coord):
                    self.game_state = 0
                    self.refresh_pic()

            # game_state 3: play list
            elif self.game_state == 3:
                if self.play_list.check_click_bob(coord):
                    self.game_state = 4
                    self.playlist = 0
                    self.track_list = TrackListScreen(self.screen_width,
                                                      self.screen_height,
                                                      "bob",
                                                      self.play_len[0])
                elif self.play_list.check_click_frozen(coord):
                    self.game_state = 4
                    self.playlist = 1
                    self.track_list = TrackListScreen(self.screen_width,
                                                      self.screen_height,
                                                      "frozen",
                                                      self.play_len[1])
                elif self.play_list.check_click_showman(coord):
                    self.game_state = 4
                    self.playlist = 2
                    self.track_list = TrackListScreen(self.screen_width,
                                                      self.screen_height,
                                                      "showman",
                                                      self.play_len[2])
                elif self.play_list.check_exit(coord):
                    self.game_state = 0
                    self.refresh_pic()

            # game_state 4: track list
            elif self.game_state == 4:
                track_no, is_clicked = self.track_list.check_click(coord)
                if is_clicked:
                    if (self.playlist == 1) and (track_no == 5):
                        self.click_pairs()
                    else:
                        self.play_track(self.playlist, track_no)
            # game_state 5: Pairs game
            elif self.game_state == 5:
                pair_state, is_clicked = self.pairs.check_click(coord)
                if pair_state == -2:
                    self.game_state = 0
                    self.refresh_pic()
            # game_state 6: Skype chat
            #               no buttons to check
            #               selenium handles all interactions

    def refresh_pic(self):
        """ redraw background picture """
        image_name = "images/backgrounds/%03d.jpg" %self.back_no
        self.image = pygame.image.load(image_name).convert()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.screen_width-self.image.get_rect().size[0])/2),
                                      max(0, (self.screen_height-self.image.get_rect().size[1])/2)))
        self.button_play.redraw()
        self.button_play_list.redraw()
        if self.button_video != None:
            self.button_video.redraw()
        if self.button_power.enabled:
            self.button_power.redraw()
        self.button_pairs.redraw()
        if self.can_we_skype():
            if self.button_skype == None:
                self.button_skype = Button(self.screen,
                                           (0,
                                            (self.screen_height / 2) - 100,
                                            200,
                                            200),
                                           "images/icons/Phone.png",
                                           (0, 0, 0))
            else:
                self.button_skype.redraw()

    def update_pic(self):
        """ change background picture """
        self.back_no += 1
        if self.back_no > 7:
            self.back_no = 1
        self.refresh_pic()

THE_GAME = MainScreen()
OLD_TIME = time.time()

while True:
    # Check power off of lights
    THE_GAME.button_power.check_off()
    # Check for event. Exit if return key pressed, otherwise pass event to THE_GAME object
    for e in pygame.event.get():
        if (e.type is pygame.KEYDOWN and e.key == pygame.K_RETURN):
            pygame.display.quit()
            exit()
        pos = pygame.mouse.get_pos()
        THE_GAME.check_event(e, pos)

    # Check for background picture of main screen changing
    if THE_GAME.game_state == 0:
        NEW_TIME = time.time()
        if (NEW_TIME - OLD_TIME) > 10:
            THE_GAME.update_pic()
            OLD_TIME = NEW_TIME
        if THE_GAME.button_power.check_button():
            THE_GAME.refresh_pic()

    if THE_GAME.play_state == 2:
        if not pygame.mixer.music.get_busy():
            if THE_GAME.can_we_play():
                THE_GAME.play_next()

    if THE_GAME.game_state == 5:
        THE_GAME.pairs.flip_back()

    if THE_GAME.game_state == 2:
        THE_GAME.video_screen.update_camera()

    pygame.display.update()
