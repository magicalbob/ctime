#!/usr/bin/env python
""" Allow Christopher to Skype us """

import time
import pygame
import os
from skpy import Skype, SkypeChats
from ctime_common import go_fullscreen
from ctime_button import Button
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class CtimeSkype(object):
    """ A Skype object """
    def __init__(self, ctime, skype_user, skype_pass):
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
        os.system('xinput set-prop 12 "Device Enabled" 0')

        """ set Chrome options """
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--kiosk")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1, 
            "profile.default_content_setting_values.notifications": 1 
        })
        """ load Chrome using selenium and get the skype page """
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://skype.ellisbs.co.uk")
        """ handle skype not being available """
        try:
          assert "Skype for Chris" in driver.title
        except:
          """ turm mouse back on, close selenium, go back to main screen """
          os.system('xinput set-prop 12 "Device Enabled" 1')
          driver.close()
          self.ctime.skype_exit = time.time()
          self.ctime.game_state = 0
          self.ctime.refresh_pic()
          go_fullscreen()
          return
        """ click the skype chat button and wait for chat frame """
        elem = driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
        """ get the chat frame and click to sign in. switch to sign in window """
        frame = driver.find_element_by_class_name("lwc-chat-frame")
        driver.switch_to.frame(frame)
        elem = driver.find_element_by_class_name("sign-in-button")
        elem.click()
        new_win=None
        old_win=driver.current_window_handle
        for win in driver.window_handles:
          if win != old_win:
            new_win=win
        driver.switch_to_window(new_win)
        """ make sign in window minimal to avoid someone clicking its controls """
        driver.set_window_size(0, 0)
        time.sleep(3)
        """ log in to skype with details from config """
        elem = driver.find_element_by_name("loginfmt")
        elem.send_keys(self.skype_user)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        elem = driver.find_element_by_name("passwd")
        elem.send_keys(self.skype_pass)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        """ go back to the original window, and reload it (login
            does not trigger auto reload) """
        driver.switch_to_window(old_win)
        driver.get("https://skype.ellisbs.co.uk")
        assert "Skype for Chris" in driver.title
        """ start the video call """
        elem = driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
        frame = driver.find_element_by_class_name("lwc-chat-frame")
        driver.switch_to.frame(frame)
        elem = driver.find_element_by_class_name("calling")
        elem.click()
        """ check the call is in progress by polling for callScreen """
        call_started = False
        call_time = time.time()
        while call_started == False:
          try:
            elem = driver.find_element_by_class_name("callScreen")
            call_started = True
            print "Call started"
          except:
            if time.time() - call_time > 30:
                """ turn mouse back on, close selenium, go back to main screen """
                os.system('xinput set-prop 12 "Device Enabled" 1')
                driver.close()
                self.ctime.skype_exit = time.time()
                self.ctime.game_state = 0
                self.ctime.refresh_pic()
                go_fullscreen()
                return


        """ now call has started, poll for it ending by looking for callScreen disappearing """
        while True:
          try:
            elem = driver.find_element_by_class_name("callScreen")
            if time.time() - call_time > 30:
                """ turn mouse back on, close selenium, go back to main screen """
                os.system('xinput set-prop 12 "Device Enabled" 1')
                driver.close()
                self.ctime.skype_exit = time.time()
                self.ctime.game_state = 0
                self.ctime.refresh_pic()
                go_fullscreen()
                return
          except:
            print "Call ended"
            """ turn mouse back on, close selenium, go back to main screen """
            os.system('xinput set-prop 12 "Device Enabled" 1')
            driver.close()
            self.ctime.skype_exit = time.time()
            self.ctime.game_state = 0
            self.ctime.refresh_pic()
            go_fullscreen()
            return
