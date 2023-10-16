#!/usr/bin/env python
""" Allow Christopher to Facebook us """

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
            self.driver = webdriver.Firefox(options=options, firefox_profile = profile)
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

    def facebook_login(self):
        """ record last time connection checked """
        self.check_connect = time.time()
        try:
            # Enter facebook username
            self.log.info('Enter facebook username')
            elem = self.driver.find_element_by_id("email")
            elem.send_keys(self.facebook_user)
            # Enter facebook password
            self.log.info('Enter facebook password')
            elem = self.driver.find_element_by_id("pass")
            elem.send_keys(self.facebook_pass)
            # Press return and wait a little
            self.log.info('Press return to logon')
            elem.send_keys(Keys.RETURN)
            time.sleep(3)
            self.driver.get(
                "https://www.facebook.com/messages/t/jackie.ellis.92?" +
                "cquick=jsc_c_n&cquick_token=AQ6FgU758TSNMWZGPcY&" +
                "ctarget=https%25253A%25252F%25252Fwww.facebook.com"
                           )
            self.mouse_change(self.ctime.enable_mouse)
        except:
            self.log.error("Facebook login failed" % e)
            self.abort_facebook()
            return

    def make_call(self):
        self.log.info('Find target for call')
    
        # Start the video chat
        self.log.info('Start the video chat')
        _ = self.driver.find_element_by_xpath('//*[@aria-label="Start a video call"]').click()
    
        """ prevent someone clicking something they shouldn't """
        self.mouse_change(self.ctime.disable_mouse)
        go_minimal()
    
        try:
            self.old_win = self.save_old_window()
        except Exception as e:
            self.log.error("could not save old window: %s" % (e))
            self.abort_facebook()
            return
    
        new_win = self.find_new_window()
        self.driver.switch_to_window(new_win)
    
        self.log.info('Start call loop')
        in_call = True
        allow_one_exception = True
    
        while in_call:
            try:
                self.check_call_status()
                if self.call_ended():
                    in_call = False
            except Exception:
                if allow_one_exception:
                    MSG = 'exception while checking still in call, give it another chance'
                    self.log.warning(MSG)
                    allow_one_exception = False
                    time.sleep(3)
                else:
                    in_call = False
                    self.log.info('exception while checking still in call, so no longer in call')
    
            if in_call:
                self.log.info('still in call so pause between checks')
                time.sleep(3)
    
        self.abort_facebook(hide_facebook=True)
    
    def save_old_window(self):
        self.log.info('save old window')
        return self.driver.current_window_handle
    
    def find_new_window(self):
        self.log.info('find new window')
        for win in self.driver.window_handles:
            if win != self.old_win:
                self.log.info('new window found')
                return win
    
    def check_call_status(self):
        self.log.info('check still in call')
        src = self.driver.page_source
        text_found = re.search(r'Please rate the quality of your video chat', src)
        if text_found:
            self.log.info('no longer in call')
            raise CallEndedException()
        text_found = re.search(r'Connection lost', src)
        if text_found:
            self.log.warning('no longer in call because of lost connection')
            raise CallEndedException()
        text_found = re.search(r'No Answer', src)
        if text_found:
            self.log.warning('no answer received, hang up')
            raise CallEndedException()
    
    def call_ended(self):
        src = self.driver.page_source
        return (
            re.search(r'Please rate the quality of your video chat', src) or
            re.search(r'Connection lost', src) or
            re.search(r'No Answer', src)
        )
    
    def check_signin(self):
        self.check_connect = time.time()
        try:
            self.driver.get("https://www.facebook.com/messages")
        except:
            self.log.error('could not get facebook for signin check')
            self.ctime.facebook = CtimeFacebook(self.ctime,
                                                self.ctime.facebook_user,
                                                self.ctime.facebook_pass)
            return
        """ handle facebook not being available """
        self.log.info('make sure facebook page loaded')
        still_logged_in = True
        try:
            assert "Facebook" in self.driver.title
            self.log.info('No longer logged in to facebook, login again')
            still_logged_in = False
            self.facebook_login()
        except AssertError:
            self.log.info('Still logged in to facebook')
        if still_logged_in == True:
            self.log.info('check that the other log in page not showing')
            src = self.driver.page_source
            text_found = re.search(
                             r'Facebook helps you connect and share with the people in your life.',
                             src
                         )
            if text_found != None:
                self.log.info('no longer really logged in to facebook, log in again')
                self.ctime.facebook = CtimeFacebook(self.ctime,
                                                    self.ctime.facebook_user,
                                                    self.ctime.facebook_pass)

    def abort_facebook(self,hide_facebook = False):
        """ turn mouse back on, close selenium, go back to main screen """
        try:
            self.log.info('turn mouse back on')
            self.mouse_change(self.ctime.enable_mouse)
            self.log.info('set time that facebook finished')
            if hide_facebook == True:
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
        except:
            self.log.error(("Faile to abort Facebook: %s", e)

    def mouse_change(self,mouse_command):
        """ prevent/enable someone clicking something they shouldn't/should """
        if mouse_command == None:
            self.log.info('No command provided for mouse')
        else:
            try:
                self.log.info("Enable/Disable the mouse with %s" % (mouse_command))
                os.system(mouse_command)
            except Exception as e:
                self.log.info("Unable to enable/disable mouse with %s: %s" % (mouse_command,e))
