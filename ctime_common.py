""" common functions for the ctime app """
import random
import pygame
import pygame.locals

def go_fullscreen():
    """ switch display to full screen mode """
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

    screen_width, screen_height = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    pygame.display.init()
    screen = pygame.display.set_mode((screen_width, screen_height), flags|pygame.FULLSCREEN, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

    return screen

def go_minimal():
    """ switch display to full screen mode """
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

    screen_width, screen_height = 0, 0

    pygame.display.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

    return screen

def shuffle_list(the_list):
    """ shuffle elements of a list into random order """
    for i, val in enumerate(the_list):
        random_number = random.randint(0, len(the_list)-1)
        the_list[i] = the_list[random_number]
        the_list[random_number] = val

    return the_list

def play_let_it_go():
    """ play favourite tune """
    try:
        pygame.mixer.init()
    except BaseException:
        print "pygame.mixer.init() failed"

    pygame.mixer.music.load("tunes/frozen/005.ogg")
    pygame.mixer.music.play()
