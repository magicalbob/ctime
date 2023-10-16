""" common functions for the ctime app """
import random
import pygame
import pygame.locals
import os
import sys

def go_fullscreen():
    """ switch display to full screen mode """
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()

    screen_width, screen_height = screen.get_width(), screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    pygame.display.init()
    try:
        screen = pygame.display.set_mode((screen_width, screen_height), flags|pygame.FULLSCREEN, bits)
    except pygame.error as e:
        screen = pygame.display.set_mode((screen_width, screen_height))
        print("An exception occurred while going full screen: %s" % e)

    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

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
    except pygame.error:
        print("pygame.mixer.init() failed")

    pygame.mixer.music.load("tunes/frozen/005.ogg")
    pygame.mixer.music.play()

def is_video_camera_present():
    if os.path.exists('/dev/video0'):
        # Linux: Check if /dev/video0 exists
        return True
    
    # macOS: Check using AVCaptureDevice
    if sys.platform == 'darwin':
        try:
            import objc
            from AVFoundation import AVCaptureDevice
            
            objc.loadBundle('AVFoundation', globals(), bundle_path=objc.pathForFramework('/System/Library/Frameworks/AVFoundation.framework'))
            
            devices = AVCaptureDevice.devices()
            for device in devices:
                if device.hasMediaType_('vide'):
                    return True
        except ImportError:
            pass
    
    return False
