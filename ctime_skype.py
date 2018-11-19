#!/usr/bin/env python
""" Allow Christopher to Skype us """

import time
import pygame
import os
import logging
import pyautogui
import subprocess
from ctime_common import go_fullscreen
from ctime_button import Button

class CtimeSkype(object):
    """ A Skype object """
    def __init__(self, ctime, skype_user, skype_pass):
        logging.info('New Skype object')
        self.screen_width = 0
        self.screen_height = 0
        self.ctime = ctime
        self.skype_user = skype_user
        self.skype_pass = skype_pass
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

        """ prevent someone clicking something they shouldn't """
        if self.ctime.disable_mouse == None:
            logging.info('No command provided to disable mouse')
        else:
            try:
                logging.info("Disable the mouse with %s" % (self.ctime.disable_mouse))
                os.system(self.ctime.disable_mouse)
            except Exception as e:
                logging.info("Unable to disable mouse: %s" % (e))

        """ load skype """
        try:
          os.system("skype")
          time.sleep(20)
          pyautogui.hotkey('alt', 'f')
          time.sleep(5)
          pyautogui.typewrite(['down','down','down','enter'])
          time.sleep(1)
          pyautogui.typewrite(['tab','tab','tab','enter'])
        except:
          pass

        """ get call start time """
        call_time = time.time()

        """ now wait up to a minute for call to start """
        call_started = False
        while (call_started == False):
            time.sleep(1)
            if time.time() - call_time > 60:
                logging.warning('call not available')
                self.abort_skype()
                return
            call_started = self.call_started()

        logging.info('call started')
        """ now wait for call to end """
        while (self.call_started()):
            time.sleep(1)

        logging.info('call ended')
        self.abort_skype(hide_skype = True)
        return

    def call_started(self):
        out = subprocess.Popen(['./countskype.sh'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        scount = int(stdout)
        logging.info("process count = %d" % scount)
        if scount < 5:
            return False
        return True

    def abort_skype(self,hide_skype = False):
        """ turn mouse back on, close skype, go back to main screen """
        logging.info('turn mouse back on')
        if self.ctime.enable_mouse == None:
            logging.info('No command provided to enable mouse')
        else:
            try:
                logging.info("Enable the mouse with %s" % (self.ctime.enable_mouse))
                os.system(self.ctime.enable_mouse)
            except Exception as e:
                logging.info("Unable to enable mouse: %s" % (e))
        logging.info('close skype')
        if os.system('pgrep skype > /dev/null') == 0:
            os.system('kill -9 $(pgrep skype) > /dev/null')
        logging.info('set time that skype finished')
        if hide_skype == True:
          self.ctime.skype_exit = time.time()
        else:
          self.ctime.skype_exit = 0
        logging.info('back to main menu game state')
        self.ctime.game_state = 0
        logging.info('re-draw main screen')
        self.ctime.refresh_pic()
        logging.info('make sure in full screen mode')
        go_fullscreen()
        logging.info('return to main screen')
