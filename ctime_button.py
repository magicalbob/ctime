""" a simple button object """

import time
import pygame

class Button(object):
    """ a simple button object """
    def __init__(self, screen, rect, image, colorkey, name, log):
        self.name = name
        self.log = log
        self.log.info('Button %s' % (self.name))
        self.rect = rect
        self.colorkey = colorkey
        self.screen = screen
        self.old_time = time.time()
        if image:
            self.log.info('Set image of Button %s' % (self.name))
            try:
                self.image = pygame.image.load(image).convert()
                self.image.set_colorkey(colorkey)
                self.screen.blit(self.image, (self.rect[0], self.rect[1]))
            except:
                self.log.error('Failed to set image of Button %s' % (self.name))
        else:
            self.image = None

    def redraw(self):
        """ redraw the button """
        if self.image != None:
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))

    def reload(self, image):
        """ reload the image of the button, in case it has changed """
        if self.image != None:
            self.image = pygame.image.load(image).convert()
            self.image.set_colorkey(self.colorkey)
            self.screen.blit(self.image, (self.rect[0], self.rect[1]))

    def change_image(self, image):
        """ change the image of the button """
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(self.colorkey)
        self.screen.blit(self.image, (self.rect[0], self.rect[1]))

    def check_click(self, pos):
        """ check if button has been pressed. stop spamming """
        return_value = False

        new_time = time.time()
        if (new_time - self.old_time) > 1:
            self.old_time = new_time
            if ((pos[0] >= self.rect[0]) and
                    (pos[0] <= self.rect[0] + self.rect[2])):
                if ((pos[1] >= self.rect[1]) and
                        (pos[1] <= self.rect[1] + self.rect[3])):
                    self.log.info('Button clicked %s' % (self.name))
                    return_value = True
        return return_value
