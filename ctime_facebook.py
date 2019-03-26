#!/usr/bio/env python
""" Allow Christopher to Facebook us """

import time
import pygame
import os
import logging
import re    
from ctime_common import go_fullscreen
from ctime_common import go_minimal
from ctime_button import Button
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class CtimeFacebook(object):
    """ A Facebook object """
    def __init__(self, ctime, facebook_user, facebook_pass):
        logging.info('New Facebook object')
        self.ctime = ctime
        self.facebook_user = facebook_user
        self.facebook_pass = facebook_pass

        """ prevent someone clicking something they shouldn't """
        self.mouse_change(self.ctime.disable_mouse)

        """ new Firefox profile - disable camera/mic permissions """
        logging.info('Create Firefox profile')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.navigator.permission.disabled", True)

        """ set Firefox options """
        logging.info('Set Firefox options')
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--new-instance")

        """ load Firefox using selenium and get the facebook page """
        logging.info('Load Firefox using selenium')
        self.driver = webdriver.Firefox(firefox_options=options, firefox_profile = profile);
        logging.info('Get facebook page')
        self.driver.get("https://www.facebook.com/messages")
        """ handle facebook not being available """
        logging.info('make sure facebook page loaded')
        try:
          assert "Log in to Facebook" in self.driver.title
        except:
          """ turn mouse back on, close selenium, go back to main screen """
          logging.error('no facebook for Chris')
          self.abort_facebook()
          return
        self.facebook_login()

    def facebook_login(self):
        """ record last time connection checked """
        self.check_connect = time.time()
        # Enter facebook username
        logging.info('Enter facebook username')
        elem = self.driver.find_element(By.XPATH,"//input[@placeholder='Email address or phone number']")
        elem.send_keys(self.facebook_user)
        # Enter facebook password
        logging.info('Enter facebook password')
        elem = self.driver.find_element(By.XPATH,"//input[@placeholder='Password']")
        elem.send_keys(self.facebook_pass)
        # Press return and wait a little
        logging.info('Press return to logon')
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

    def make_call(self):
        logging.info('Find target for call')
        try:
          # Find Jackie
          elem = self.driver.find_element_by_id("row_header_id_user:1464426309")
#          elem = self.driver.find_element_by_id("row_header_id_user:794646869")
          logging.info('Target for call found')
        except:
          logging.warning('Target for call not found at first, try again')
          time.sleep(3)
          # Find Jackie
          elem = self.driver.find_element_by_id("row_header_id_user:1464426309")
#          elem = self.driver.find_element_by_id("row_header_id_user:794646869")
          logging.error('Target for call still not found')
          self.abort_facebook()
          return

        # Select the target
        logging.info('Click target')
        elem.click()
        # Start the video chat
        logging.info('Start the video chat')
        elem = self.driver.find_element_by_xpath('//*[@title="Start a video chat"]').click()
        """ prevent someone clicking something they shouldn't """
        self.mouse_change(self.ctime.disable_mouse)
        go_minimal()

        self.old_win = None
        try:
          logging.info('save old window')
          self.old_win=self.driver.current_window_handle
        except Exception as e:
          logging.error("could not save old window: %s" % (e))
          self.abort_facebook()
          return
        logging.info('find new window')
        new_win=None
        for win in self.driver.window_handles:
          if win != self.old_win:
            logging.info('new window found')
            new_win=win
        self.driver.switch_to_window(new_win)

        logging.info('Start call loop')
        inCall = True
        allow_one_exception = True
        while inCall == True:
            try:
                logging.info('check still in call')
                src = self.driver.page_source
                text_found = re.search(r'Please rate the quality of your video call', src)
                if text_found != None:
                    logging.info('no longer in call')
                    inCall = False
                text_found = re.search(r'Connection lost', src)
                if text_found != None:
                    logging.warning('no longer in call because of lost connection')
                    inCall = False
                text_found = re.search(r'No Answer', src)
                if text_found != None:
                    logging.warning('no answer received, hang up')
                    inCall = False
            except:
                if allow_one_exception == True:
                    logging.warning('exception while checking still in call, give it another chance')
                    allow_one_exception = False
                    time.sleep(3)
                else:
                    inCall = False
                    logging.info('exception while checking still in call, so no longer in call')
            if inCall == True:
              logging.info('still in call so pause between checks')
              time.sleep(3)
        self.abort_facebook(hide_facebook = True)

    def check_signin(self):
        self.check_connect = time.time()
        try:
          self.driver.get("https://www.facebook.com/messages")
        except:
          logging.error('could not get facebook for signin check')
          self.ctime.facebook = CtimeFacebook(self.ctime,
                                              self.ctime.facebook_user,
                                              self.ctime.facebook_pass)
          return
        """ handle facebook not being available """
        logging.info('make sure facebook page loaded')
        still_logged_in = True
        try:
          assert "Log in to Facebook" in self.driver.title
          logging.info('No longer logged in to facebook, login again')
          still_logged_in = False
          self.facebook_login()
        except:
          logging.info('Still logged in to facebook')
        if still_logged_in == True:
          logging.info('check that the other log in page not showing')
          src = self.driver.page_source
          text_found = re.search(r'Facebook helps you connect and share with the people in your life.', src)
          if text_found != None:
            logging.info('no longer really logged in to facebook, log in again')
            self.ctime.facebook = CtimeFacebook(self.ctime,
                                                self.ctime.facebook_user,
                                                self.ctime.facebook_pass)

    def abort_facebook(self,hide_facebook = False):
        """ turn mouse back on, close selenium, go back to main screen """
        logging.info('turn mouse back on')
        self.mouse_change(self.ctime.enable_mouse)
        logging.info('set time that facebook finished')
        if hide_facebook == True:
          logging.info('set actual time cos facebook needs to hide')
          self.ctime.facebook_exit = time.time()
        else:
          logging.info('set no time cos facebook went wrong so no hide')
          self.ctime.facebook_exit = 0
        logging.info('go back to old window')
        self.driver.switch_to_window(self.old_win)
        logging.info('back to main menu game state')
        self.ctime.game_state = 0
        logging.info('re-draw main screen')
        self.ctime.refresh_pic()
        logging.info('make sure in full screen mode')
        go_fullscreen()
        logging.info('return to main screen')

    def mouse_change(self,mouse_command):
        """ prevent/enable someone clicking something they shouldn't/should """
        if mouse_command == None:
            logging.info('No command provided for mouse')
        else:
            try:
                logging.info("Enable/Disable the mouse with %s" % (mouse_command))
                os.system(mouse_command)
            except Exception as e:
                logging.info("Unable to enable/disable mouse with %s: %s" % (mouse_command,e))
