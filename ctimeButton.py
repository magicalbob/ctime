import time
import pygame

class button:
        def __init__(self, screen, rect, image, colorkey):
                self.rect=rect
                self.colorkey=colorkey
                self.image=pygame.image.load(image).convert()
                self.image.set_colorkey(colorkey)
                self.screen=screen
                self.screen.blit(self.image,(self.rect[0], self.rect[1]))
                self.oTime = time.time()

        def redraw(self):
                self.screen.blit(self.image,(self.rect[0], self.rect[1]))

        def changeImage(self, image):
                self.image=pygame.image.load(image).convert()
                self.image.set_colorkey(self.colorkey) 
                self.screen.blit(self.image, (self.rect[0], self.rect[1]))

        def checkClick(self, pos):
                retVal = False

                nTime = time.time()
                if (nTime - self.oTime) > 1:
                        self.oTime = nTime
                        if ((pos[0] >= self.rect[0]) and
                            (pos[0] <= self.rect[0] + self.rect[2])):
                                if ((pos[1] >= self.rect[1]) and
                                    (pos[1] <= self.rect[1] + self.rect[3])):
                                        retVal = True
                return retVal


