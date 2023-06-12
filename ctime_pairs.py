""" a simple pairs game based on frozen """
import time
import os
import pygame
import pygame.locals
from ctime_button import Button
from ctime_common import shuffle_list
from ctime_common import go_fullscreen
from ctime_common import play_let_it_go

class PairsScreen():
    """ class for simple pairs game """
    def __init__(self, screen_width, screen_height, ctime, new_game = True):
        self.log = ctime.log
        self.log.info('New PairsScreen')
        self.screen_size = {'width': screen_width,
                            'height': screen_height}
        self.screen = pygame.display.get_surface()
        self.screen.fill(pygame.Color(0, 0, 0, 0),
                         (0, 0, self.screen_size['width'], self.screen_size['height']),
                         0)
        go_fullscreen()

        self.cards = {'count': 8, 'list': [], 'back': [], 'clicked': [-1, -1]}
        self.flip_time = 0

        if new_game == True:
            self.log.info('New pairs game. No exit button')
            self.button_exit = None
        else:
            self.log.info('Another pairs game. Add exit button')
            self.add_button_exit()

        self.ctime = ctime

        card_index = 0
        while card_index < self.cards['count']:
            x_pos, y_pos = self.get_button_pos(card_index)
            self.cards['list'].append(
                Button(self.screen,
                       (x_pos, y_pos, 200, 400),
                       "images/pairs/Snowflake.png",
                       (0, 0, 0),
                       "CardButton%s" % (card_index),
                       self.log)
            )
            self.cards['list'][card_index].colorkey = (255, 255, 255)
            self.cards['list'][card_index].cardDone = False
            card_index += 1

        for i in range(self.cards['count']):
            self.cards['back'].append(i % (self.cards['count'] / 2))

        self.cards['back'] = shuffle_list(self.cards['back'])

        self.draw_facebook()

    def redraw(self):
        """ redraw the cards in their current state """
        self.log.info('Redraw the cards in their current state')
        self.screen = pygame.display.get_surface()
        self.screen.fill(pygame.Color(0, 0, 0, 0),
                         (0, 0, self.screen_size['width'], self.screen_size['height']),
                         0)
        if os.uname()[1].startswith('rpi'):
            go_fullscreen()

        self.log.info('If exit button set, redraw it')
        if self.button_exit != None:
            self.log.info('Redraw exit button')
            self.button_exit.redraw()

        for card_index in range(self.cards['count']):
            save_done = self.cards['list'][card_index].cardDone
            x_pos, y_pos = self.get_button_pos(card_index)
            if save_done:
                image = ""
            else:
                image = "images/pairs/Snowflake.png"
            self.cards['list'][card_index] = Button(self.screen,
                                                    (x_pos, y_pos, 200, 400),
                                                    image,
                                                    (0, 0, 0),
                                                    "CardButton%s" % (card_index),
                                                    self.log)
            self.cards['list'][card_index].colorkey = (255, 255, 255)
            self.cards['list'][card_index].cardDone = save_done

        self.draw_facebook()

    def draw_facebook(self):
        if self.ctime.can_we_facebook():
            self.button_facebook = Button(self.screen,
                                          (self.screen_size['width'] - 200,
                                           self.screen_size['height'] - 200,
                                           200,
                                           200),
                                          "images/icons/Phone.png",
                                          (0, 0, 0),
                                          "FacebookButton",
                                          self.log)
        else:
            self.button_facebook = None

    def add_button_exit(self):
        self.button_exit = Button(self.screen,
                                  (self.screen_size['width'] - 200, 0, 200, 200),
                                  "images/icons/StopButton.png",
                                  (0, 0, 0),
                                  "FacebookExit",
                                  self.log)

    def get_button_pos(self, button_no):
        """ get the x,y position of a button by number """
        button_col = button_no % 4
        button_row = int(button_no / 4)

        pad_x = (self.screen_size['width'] - 800) / 6
        pad_y = (self.screen_size['height'] - 800) / 3

        return [pad_x + (button_col * (200 + pad_x)), pad_y + (button_row * (400 + pad_y))]

    def flip_card(self, card_num):
        """ turn a card over """
        self.log.info("Turn a card over: %d" % (card_num))
        if self.cards['clicked'][0] == -1:
            self.cards['clicked'][0] = card_num
            self.cards['list'][card_num].reload(
                "images/pairs/card%d.png" % (self.cards['back'][card_num]))
        else:
            if self.cards['clicked'][0] == card_num:
                pass
            elif self.cards['clicked'][1] == -1:
                self.cards['clicked'][1] = card_num
                self.cards['list'][card_num].reload("images/pairs/card%d.png" %
                                                    (self.cards['back'][card_num]))
                self.flip_time = time.time()
                if self.cards['back'][
                        self.cards['clicked'][0]] == self.cards['back'][self.cards['clicked'][1]]:
                    self.cards['list'][self.cards['clicked'][0]].cardDone = True
                    self.cards['list'][self.cards['clicked'][1]].cardDone = True
                    self.play_success()

    def flip_back(self):
        """ turn a card back to back showing """
        if self.cards['clicked'][1] != -1:
            if time.time() - self.flip_time > 3:
                if not self.cards['list'][self.cards['clicked'][0]].cardDone:
                    self.cards['list'][
                        self.cards['clicked'][0]].reload("images/pairs/Snowflake.png")
                    self.cards['list'][
                        self.cards['clicked'][1]].reload("images/pairs/Snowflake.png")
                self.cards['clicked'] = [-1, -1]

    def check_click(self, pos):
        """ check if exit button has been clicked """
        if self.button_exit != None:
            if self.button_exit.check_click(pos):
                return [-2, False]

        """ check if facebook button has been clicked """
        if self.button_facebook != None:
            if self.button_facebook.check_click(pos):
                self.log.info('button_facebook clicked')
                self.ctime.button_facebook = None
                self.button_facebook = None
                self.redraw()
                self.ctime.click_facebook()

        """ check if a card has been clicked """
        for card_index in range(self.cards['count']):
            if self.cards['list'][card_index].check_click(pos):
                if not self.cards['list'][card_index].cardDone:
                    self.flip_card(card_index)
                    return [card_index, True]
        return [-1, False]

    def play_success(self):
        """ player won a match. celebrate! """
        pygame.display.update()
        play_applause()
        time.sleep(6)
        if self.button_exit is None:
            self.add_button_exit()
        play_let_it_go()
        for card_index in range(self.cards['count']):
            if not self.cards['list'][card_index].cardDone:
                self.redraw()
                return
        """ All cards are done, so start new game """
        self.__init__(self.screen_size['width'], self.screen_size['height'], False)

def play_applause():
    """ clapping used in celebration """
    try:
        pygame.mixer.init()
    except BaseException:
        self.log.error('pygame.mixer.init() failed')
    new_tune = "sounds/applause.ogg"
    pygame.mixer.music.load(new_tune)
    pygame.mixer.music.play()
