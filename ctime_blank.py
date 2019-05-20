""" blank screen to stop game being played out-of-hours """
import random
import os
import pygame
import pygame.locals
import logging
from ctime_common import go_fullscreen

class BlankScreen(object):
    """ a blank screen with no controls """
    def __init__(self, ctime, screen_width, screen_height):
        logging.info('Time for bed said Zeberdee')
        self.screen_size = {'width': screen_width, 'height': screen_height}
        self.screen = pygame.display.get_surface()
        self.screen.fill(pygame.Color(0, 0, 0, 0),
                         (0, 0, screen_width, screen_height),
                         0)
        logging.info('Lights out')
        ctime.button_power.rpi_power()
        go_fullscreen()
