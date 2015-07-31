import unittest
from ctimeButton import button 
import pygame

class testcases(unittest.TestCase):
  def setUp(self):
    self.screen = screen = pygame.display.set_mode()

  def tearDown(self):
    pass

  def test01(self):
    self.button = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
    assert self.button.rect[0] == 0

  def test02(self):
    self.button = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
    assert self.button.rect[1] == 0

  def test03(self):
    self.button = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
    assert self.button.rect[2] == 200

  def test04(self):
    self.button = button(self.screen, (0,0,200,200), "images/icons/PlayButton.png",(0,0,0))
    assert self.button.rect[3] == 200

if __name__ == "__main__":
  unittest.main() # run all tests
