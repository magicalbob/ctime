import pygame
from pygame.locals import *
import random

def go_fullscreen():
  screen = pygame.display.get_surface()
  tmp = screen.convert()
  caption = pygame.display.get_caption()
  cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007
  
  w,h = screen.get_width(),screen.get_height()
  flags = screen.get_flags()
  bits = screen.get_bitsize()

  pygame.display.init()
  screen = pygame.display.set_mode((w,h),flags|FULLSCREEN,bits)
  screen.blit(tmp,(0,0))
  pygame.display.set_caption(*caption)

  pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

  pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

  return screen

def shuffleList(theList):
  for i,val in enumerate(theList):
    randNum=random.randint(0,len(theList)-1)
    theList[i]=theList[randNum]
    theList[randNum]=val

  return theList
