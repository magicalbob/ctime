#!/usr/bin/env python
""" Allow Christopher to Skype us """

import time
import pygame
import os
import logging
from ctime_common import go_fullscreen
from ctime_button import Button
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        self.mouse_change(self.ctime.disable_mouse)
        """ set Chrome options """
        logging.info('Set Chrome options')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1, 
            "profile.default_content_setting_values.notifications": 1 
        })
        """ load Chrome using selenium and get the skype page """
        logging.info('Load Chrome using selenium')
        self.driver = webdriver.Chrome(chrome_options=options)
        logging.info('Get skype page')
        self.driver.get("https://skype.ellisbs.co.uk")
        """ handle skype not being available """
        logging.info('make sure skype page loaded')
        try:
          assert "Skype for Chris" in self.driver.title
        except:
          """ turn mouse back on, close selenium, go back to main screen """
          logging.error('no skype for Chris')
          self.abort_skype()
          return
        """ click the skype chat button and wait for chat frame """
        logging.info('click the skype chat button')
        elem = self.driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
        """ get the chat frame and click to sign in. switch to sign in window """
        logging.info('get the chat frame')
        try:
          frame = self.driver.find_element_by_class_name("lwc-chat-frame")
          self.driver.switch_to.frame(frame)
        except Exception as e:
          logging.error("could not switch to lwc-chat-frame: %s" % (e))
          self.abort_skype()
          return
        do_login=True
        try:
          logging.info('click sign in button')
          elem = self.driver.find_element_by_class_name("sign-in-button")
          elem.click()
        except:
          logging.info('already signed in?')
          do_login = False
        old_win = None
        try:
          logging.info('save old window')
          old_win=self.driver.current_window_handle
        except Exception as e:
          logging.error("could not save old window: %s" % (e))
          self.abort_skype()
          return
        if do_login==True:
          logging.info('log in')
          new_win=None
          logging.info('find log in window')
          for win in self.driver.window_handles:
            if win != old_win:
              new_win=win
          logging.info('switch to log in window')
          self.driver.switch_to_window(new_win)
          """ make sign in window minimal to avoid someone clicking its controls """
          logging.info('minimise log in window')
          self.driver.set_window_size(0, 0)
          time.sleep(3)
          """ log in to skype with details from config """
          logging.info('enter log in id')
          elem = self.driver.find_element_by_name("loginfmt")
          elem.send_keys(self.skype_user)
          elem.send_keys(Keys.RETURN)
          time.sleep(3)
          logging.info('enter password')
          elem = self.driver.find_element_by_name("passwd")
          elem.send_keys(self.skype_pass)
          elem.send_keys(Keys.RETURN)
          time.sleep(3)
        """ go back to the original window, and reload it (login
            does not trigger auto reload) """
        logging.info('back to chat window')
        self.driver.switch_to_window(old_win)
        logging.info('reload skype page')
        self.driver.get("https://skype.ellisbs.co.uk")
        logging.info('check skype page re-loaded')
        try:
          assert "Skype for Chris" in self.driver.title
        except:
          """ turn mouse back on, close selenium, go back to main screen """
          logging.error('reload of skype for Chris failed')
          self.abort_skype()
          return
        """ start the video call """
        logging.info('start video call')
        elem = self.driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
        logging.info('switch to chat frame')
        frame = self.driver.find_element_by_class_name("lwc-chat-frame")
        self.driver.switch_to.frame(frame)
        logging.info('click calling')
        found_calling=False
        call_time = time.time()
        while found_calling == False:
          try:
            elem = self.driver.find_element_by_xpath('//*[@title="Start a video call"]').click()
            found_calling = True
          except Exception as e:
            logging.error("calling not available: %s" % (e))
            time.sleep(1)
            if time.time() - call_time > 5:
                logging.warning('call not available')
                logging.warning(self.driver.page_source)
                self.abort_skype()
                return

        """ check the call is in progress by polling for callScreen """
        call_started = False
        call_time = time.time()
        logging.info('wait for call to start')
        while call_started == False:
          try:
            elem = self.driver.find_element_by_class_name("callScreen")
            call_started = True
            logging.info('Call started')
          except:
            if time.time() - call_time > 90:
                logging.warning('call failed to start')
                self.abort_skype()
                return
        
        """ now call has started, poll for it ending by looking for callScreen disappearing """
        logging.info('wait for call screen to disappear to wrap up')
        while True:
          try:
            elem = self.driver.find_element_by_class_name("callScreen")
          except:
            logging.info('Call ended')
            self.abort_skype(hide_skype = True)
            return

        try:
          logging.info('close selenium')
          self.driver.close()
        except:
          logging.info('selenium close failed?')

    def abort_skype(self,hide_skype = False):
        """ turn mouse back on, close selenium, go back to main screen """
        logging.info('closing down skype')
        self.mouse_change(self.ctime.enable_mouse)
        logging.info('close selenium driver')
        try:
          self.driver.close()
        except:
          logging.warning('selenium driver did not like closing')
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
