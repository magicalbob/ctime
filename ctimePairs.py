import pygame
import random
import time
import os
from pygame.locals import *
from ctimeCommon import shuffleList
from ctimeButton import button
from ctimeCommon import go_fullscreen


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
    self.cardClicked = [-1,-1]
    self.flipTime = 0

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
      self.cardList[cardIdx].colorkey=(255,255,255)
      self.cardList[cardIdx].cardDone=False
      cardIdx += 1

    for i in range(self.cardCount):
      self.cardBack.append(i % (self.cardCount / 2))

    self.cardBack=shuffleList(self.cardBack)
         
  def redraw(self):
    self.screen = pygame.display.get_surface()
    self.screen.fill(Color(0,0,0,0), (0,0,self.sWidth,self.sHeight), 0)
    go_fullscreen()

    self.buttonExit.redraw()

    for cardIdx in range(self.cardCount):
      saveDone=self.cardList[cardIdx].cardDone
      xPos, yPos = self.getButtonPos(cardIdx)
      if saveDone==True:
        image="images/pairs/card%d.png" % (self.cardBack[cardIdx])
      else:
        image="images/pairs/Snowflake.png"
      self.cardList[cardIdx]= button(self.screen,
             (xPos,yPos,200,400),
             image,
             (0,0,0))
      self.cardList[cardIdx].colorkey=(255,255,255)
      self.cardList[cardIdx].cardDone=saveDone

  def getButtonPos(self, buttonNo):
    bCol = buttonNo % 4
    bRow = buttonNo / 4

    padX = (self.sWidth - 800) / 6
    padY = (self.sHeight - 800) / 3    

    return [ padX + (bCol * (200 + padX)), padY + (bRow * (400 + padY)) ]

  def flipCard(self, cardNum):
    if self.cardClicked[0]==-1:
      self.cardClicked[0]=cardNum
      self.cardList[cardNum].reload("images/pairs/card%d.png" % (self.cardBack[cardNum]))
    else:
      if self.cardClicked[0]==cardNum:
        pass
      elif self.cardClicked[1] == -1:
        self.cardClicked[1]=cardNum
        self.cardList[cardNum].reload("images/pairs/card%d.png" % (self.cardBack[cardNum]))
        self.flipTime=time.time()
        if self.cardBack[self.cardClicked[0]] == self.cardBack[self.cardClicked[1]]:
          self.cardList[self.cardClicked[0]].cardDone = True
          self.cardList[self.cardClicked[1]].cardDone = True
          pygame.display.update()
          self.playApplause()
          time.sleep(6)
          if (os.uname()[1] == 'rpi21'):
            self.playVideo()
          else:
            print("Can only play video on Pi")

  def flipBack(self):
    if self.cardClicked[1] != -1:
      nTime = time.time()
      if nTime - self.flipTime > 3:
        if self.cardList[self.cardClicked[0]].cardDone == False:
          self.cardList[self.cardClicked[0]].reload("images/pairs/Snowflake.png")
          self.cardList[self.cardClicked[1]].reload("images/pairs/Snowflake.png")
        self.cardClicked=[-1,-1]

  def checkClick(self, pos):
    if self.buttonExit.checkClick(pos):
      return [-2, False]

    for cardIdx in range(self.cardCount):
      if self.cardList[cardIdx].checkClick(pos):
        if self.cardList[cardIdx].cardDone==False:
          self.flipCard(cardIdx)
          return [ cardIdx, True ]
    return [ -1, False ]

  def playVideo(self):
    pygame.mixer.quit()
    pygame.display.set_mode([self.sWidth,self.sHeight])
    movieName = "videos/%03d.MPG" %random.randint(1,3)
    os.system("mplayer -fs %s" % (movieName))
    go_fullscreen()
    for cardIdx in range(self.cardCount):
      if self.cardList[cardIdx].cardDone==False:
        self.redraw()
        return
    self.__init__(self.sWidth,self.sHeight)

  def playApplause(self):
    try:
      pygame.mixer.init()
    except:
      print "pygame.mixer.init() failed"
    newTune = "sounds/applause.ogg"
    pygame.mixer.music.load(newTune)
    pygame.mixer.music.play()
