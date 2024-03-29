""" allow play lists and tracks to be selected """
import random
import os
import pygame
import pygame.locals
from src.ctime.ctime_common import go_fullscreen
from src.ctime.ctime_common import shuffle_list
from src.ctime.ctime_button import Button

IMAGES_ICONS = 'images/icons/%s.png'

class TrackListScreen():
    """ list tracks to select """
    def __init__(self, screen_width, screen_height, play_list, tracks, log):
        """ initialise track list """
        self.log = log

        self.screen_size = {'width': screen_width, 'height': screen_height}
        self.screen = pygame.display.get_surface()
        self.screen.fill(pygame.Color(0, 0, 0, 0),
                         (0, 0, screen_width, screen_height),
                         0)
        go_fullscreen()

        self.play_list = play_list
        self.tracks = tracks
        self.track_list = []

        track_random = []
        for track_index in range(0, self.tracks):
            track_random.append(self.get_button_pos(track_index))
        track_random = shuffle_list(track_random)

        track_index = 0
        while track_index < self.tracks:
            x_pos, y_pos = track_random[track_index]
            self.track_list.append(Button(self.screen,
                                          (x_pos, y_pos, 150, 150),
                                          "images/icons/%s/%03d.png" % (play_list,
                                                                        track_index+1),
                                          (0, 0, 0),
                                          "Track%s" % (track_index),
                                          self.log))
            track_index += 1

    def get_button_pos(self, button_no):
        """ get x,y position of button by number """
        button_col = button_no % 8
        button_row = int(button_no / 8)

        pad_x = (self.screen_size['width'] - 1200) / 9
        pad_y = (self.screen_size['height'] - 600) / 5

        return [pad_x + (button_col * (150 + pad_x)), pad_y + (button_row * (150 + pad_y))]

    def check_click(self, pos):
        """ check if track clicked, and which one """
        track_index = 0
        while track_index < self.tracks:
            if self.track_list[track_index].check_click(pos):
                return [track_index + 1, True]
            track_index += 1
        return [-1, False]

class PlayListScreen(object):
    """ allow play lists to be selected """
    def __init__(self, screen_width, screen_height, log):
        """ initalise play list """
        self.log = log
        self.screen = pygame.display.get_surface()
        self.screen.fill(pygame.Color(0, 0, 0, 0),
                         (0, 0, screen_width, screen_height),
                         0)
        go_fullscreen()

        button_position = []
        button_position.append(((screen_width / 4) - 100,
                                (screen_height / 3) - 100,
                                200,
                                200))
        button_position.append((((screen_width * 3) / 4) - 100,
                                (screen_height / 3) - 100,
                                200,
                                200))
        button_position.append(((screen_width / 4) - 100,
                                (2 * screen_height / 3) - 100,
                                200,
                                200))

        button_space = [0, 1, 2]
        button_instance = []
        button_select = random.randint(0,2)
        button_instance.append(button_space[button_select])
        button_space.pop(button_select)
        button_select = random.randint(0,1)
        button_instance.append(button_space[button_select])
        button_space.pop(button_select)
        button_instance.append(button_space[0])

        self.button_exit = Button(self.screen,
                                  (screen_width - 200, 0, 200, 200),
                                  "images/icons/StopButton.png",
                                  (0, 0, 0),
                                  "TrackListExit",
                                  self.log)

        self.button_bob = Button(self.screen,
                                 button_position[button_instance[0]],
                                 IMAGES_ICONS % ("bob"),
                                 (0, 0, 0),
                                 "Bob",
                                 self.log)

        self.button_frozen = Button(self.screen,
                                    button_position[button_instance[1]],
                                    IMAGES_ICONS % ("frozen"),
                                    (0, 0, 0),
                                    "Frozen",
                                    self.log)

        self.button_showman = Button(self.screen,
                                     button_position[button_instance[2]],
                                     IMAGES_ICONS % ("showman"),
                                     (0, 0, 0),
                                     "Showman",
                                     self.log)

    def check_click_bob(self, pos):
        """ has bob been clicked """
        if self.button_bob.check_click(pos):
            return True
        return False

    def check_click_frozen(self, pos):
        """ has frozen been clicked """
        if self.button_frozen.check_click(pos):
            return True
        return False

    def check_click_showman(self, pos):
        """ has showman been clicked """
        if self.button_showman.check_click(pos):
            return True
        return False

    def check_exit(self, pos):
        """ has exit button been pressed """
        if self.button_exit.check_click(pos):
            return True
        return False
