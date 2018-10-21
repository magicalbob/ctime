#!/usr/bin/env python
""" Allow Christopher to Skype us """

import time
import pygame
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

        self.button_exit = Button(self.screen,
                                  (self.screen_width - 200, 0, 200, 200),
                                  "images/icons/StopButton.png",
                                  (0, 0, 0))
        self.re_init()

    def re_init(self):
        """ re-initialise the screen - used when sub screen closes """
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
        driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://skype.ellisbs.co.uk")
        try:
          assert "Skype for Chris" in driver.title
        except:
          driver.close()
          self.ctime.game_state = 0
          self.ctime.refresh_pic()
          go_fullscreen()
          return
        elem = driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
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
        driver.set_window_size(0, 0)
        time.sleep(3)
        elem = driver.find_element_by_name("loginfmt")
        elem.send_keys(self.skype_user)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        elem = driver.find_element_by_name("passwd")
        elem.send_keys(self.skype_pass)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.switch_to_window(old_win)
        driver.get("https://skype.ellisbs.co.uk")
        assert "Skype for Chris" in driver.title
        elem = driver.find_element_by_class_name("lwc-chat-button")
        elem.click()
        time.sleep(3)
        frame = driver.find_element_by_class_name("lwc-chat-frame")
        driver.switch_to.frame(frame)
        elem = driver.find_element_by_class_name("calling")
        elem.click()
        call_started = False
        while call_started == False:
          try:
            elem = driver.find_element_by_class_name("callScreen")
            call_started = True
            print "Call started"
          except:
            pass

        while True:
          try:
            elem = driver.find_element_by_class_name("callScreen")
          except:
            print "Call ended"
            driver.close()
            self.ctime.game_state = 0
            self.ctime.refresh_pic()
            go_fullscreen()
            return


    def check_click(self, pos):
        """ check if exit has been clicked """
        if self.button_exit.check_click(pos):
            go_fullscreen()
            return True

        return False


