import time
import pygame
import os
import re
from src.ctime.ctime_common import go_fullscreen
from src.ctime.ctime_common import go_minimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class CallEndedException(Exception):
    pass

class CtimeFacebook():
    """ A Facebook object """
    def __init__(self, ctime, facebook_user, facebook_pass, log):
        self.log = log
        self.log.info('New Facebook object')
        self.ctime = ctime
        self.facebook_user = facebook_user
        self.facebook_pass = facebook_pass

        """ prevent someone clicking something they shouldn't """
        self.mouse_change(self.ctime.disable_mouse)

        print("DEBUG: new Firefox profile - disable camera/mic permissions ")
        """ new Firefox profile - disable camera/mic permissions """
        self.log.info('Create Firefox profile')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.navigator.permission.disabled", True)

        print("DEBUG: set Firefox options ")
        """ set Firefox options """
        self.log.info('Set Firefox options')
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--new-instance")

        print("DEBUG: load Firefox using selenium and get the facebook page ")
        """ load Firefox using selenium and get the facebook page """
        self.log.info('Load Firefox using selenium')
        try:
            self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
            print("DEBUG: Get facebook page")
            self.log.info('Get facebook page')
            self.driver.get("https://www.facebook.com/messages")
        except Exception as e:
            self.log.error("Failed to initialize Facebook: %s" % e)
            self.abort_facebook()
            return

        print("DEBUG: handle facebook not being available ")
        """ handle facebook not being available """
        self.log.info('make sure facebook page loaded')
        try:
            assert "Facebook" in self.driver.title
        except AssertionError:
            """ turn mouse back on, close selenium, go back to main screen """
            self.log.error('no facebook for Chris')
            self.abort_facebook()
            return
        print("DEBUG: try facebook login")
        self.facebook_login()
        print("DEBUG: facebook login done")

    # ... (rest of the code remains the same)

    def abort_facebook(self, hide_facebook=False):
        """ turn mouse back on, close selenium, go back to main screen """
        try:
            self.log.info('turn mouse back on')
            self.mouse_change(self.ctime.enable_mouse)
            self.log.info('set time that facebook finished')
            if hide_facebook:
                self.log.info('set actual time cos facebook needs to hide')
                self.ctime.facebook_exit = time.time()
            else:
                self.log.info('set no time cos facebook went wrong so no hide')
                self.ctime.facebook_exit = 0
            self.log.info('go back to old window')
            self.driver.switch_to_window(self.old_win)
            self.log.info('back to main menu game state')
            self.ctime.game_state = 0
            self.log.info('re-draw main screen')
            self.ctime.refresh_pic()
            self.log.info('make sure in full screen mode')
            go_fullscreen()
            self.log.info('return to main screen')
        except Exception as e:
            self.log.error("Failed to abort Facebook: %s" % e)

    def mouse_change(self, mouse_command):
        """ prevent/enable someone clicking something they shouldn't/should """
        if mouse_command is None:
            self.log.info('No command provided for mouse')
        else:
            try:
                self.log.info("Enable/Disable the mouse with %s" % (mouse_command))
                os.system(mouse_command)
            except Exception as e:
                self.log.info("Unable to enable/disable mouse with %s: %s" % (mouse_command, e))

