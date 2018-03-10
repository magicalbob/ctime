""" test of button object """
import unittest
import pygame
from ctime_button import Button

class TestCases(unittest.TestCase):
    """ unit test of button """
    def __init__(self, *args, **kwargs):
        """ initialise the Test Case """
        super(TestCases, self).__init__(*args, **kwargs)
        self.button = None

    def setUp(self):
        """ set up a screen for the button """
        self.screen = pygame.display.set_mode()

    def tearDown(self):
        """ don't do anything yet """
        pass

    def test01(self):
        """ test button at correct x location """
        self.button = Button(self.screen,
                             (0, 0, 200, 200),
                             "images/icons/PlayButton.png",
                             (0, 0, 0))
        assert self.button.rect[0] == 0

    def test02(self):
        """ test button at correct y location """
        self.button = Button(self.screen,
                             (0, 0, 200, 200),
                             "images/icons/PlayButton.png",
                             (0, 0, 0))
        assert self.button.rect[1] == 0

    def test03(self):
        """ test button has correct width """
        self.button = Button(self.screen,
                             (0, 0, 200, 200),
                             "images/icons/PlayButton.png",
                             (0, 0, 0))
        assert self.button.rect[2] == 200

    def test04(self):
        """ test button has correct height """
        self.button = Button(self.screen,
                             (0, 0, 200, 200),
                             "images/icons/PlayButton.png",
                             (0, 0, 0))
        assert self.button.rect[3] == 200

if __name__ == "__main__":
    unittest.main() # run all tests
