import pygame
from pygame.locals import *
from ctimeCommon import go_fullscreen
from ctimeCommon import shuffleList
from ctimeButton import button

class pairsScreen:
  def __init__(self, sWidth, sHeight):
    self.sWidth = sWidth
    self.sHeight = sHeight
    self.screen = pygame.display.get_surface()
    self.screen.fill(Color(0,0,0,0), (0,0,sWidth,sHeight), 0)
    self.gameState=5
    go_fullscreen()

    self.cardCount = 8
    self.cardList = []
    self.cardBack = []

    self.buttonExit = button(self.screen,
		             (self.sWidth - 200,0,200,200),
		             "images/icons/StopButton.png",
		             (0,0,0))

    cardIdx = 0
    while cardIdx < self.cardCount:
      xPos, yPos = self.getButtonPos(cardIdx)
      self.cardList.append(
        button(self.screen,
               (xPos,yPos,200,400),
               "images/pairs/Snowflake.png",
               (0,0,0))
      )
      cardIdx += 1

    for i in range(self.cardCount):
      self.cardBack.append(i % (self.cardCount / 2))

    self.cardBack=shuffleList(self.cardBack)
         
  def getButtonPos(self, buttonNo):
    bCol = buttonNo % 4
    bRow = buttonNo / 4

    padX = (self.sWidth - 800) / 6
    padY = (self.sHeight - 800) / 3    

    return [ padX + (bCol * (200 + padX)), padY + (bRow * (400 + padY)) ]

  def checkClick(self, pos):
    cardIdx = 0
    while cardIdx < self.cardCount:
      if self.cardList[cardIdx].checkClick(pos):
        return [ CardIdx + 1, True ]
      cardIdx += 1
    return [ -1, False ]
