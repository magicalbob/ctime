#!/usr/bin/env python
""" Allow Christopher to Skype us """

import time
import pygame
from skpy import Skype, SkypeChats
from ctime_common import go_fullscreen
from ctime_button import Button

class CtimeSkype(object):
    """ A Skype object """
    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = screen.get_width(), screen.get_height()

        self.image = pygame.image.load("images/backgrounds/001.jpg").convert()
        self.button_exit = Button(self.screen,

                                  (self.screen_width - 200, 0, 200, 200),
                                  "images/icons/StopButton.png",
                                  (0, 0, 0))
        self.re_init()

    def re_init(self):
        """ re-initialise the screen - used when sub screen closes """
        self.game_state = 0
        go_fullscreen()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (max(0, (self.screen_width-self.image.get_rect().size[0])/2),
                                      max(0, (self.screen_height-self.image.get_rect().size[1])/2)))
        self.button_exit.redraw()
        pygame.display.update()
