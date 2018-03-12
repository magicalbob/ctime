""" handle display of usb camera """
import logging
import pygame
import pygame.camera
import pygame.locals
from ctime_common import go_fullscreen
from ctime_button import Button

class Camera(object):
    """ object to display usb camera """
    def __init__(self, screen_width, screen_height, path):
        self.screen_size = {'width': screen_width, 'height': screen_height}
        self.path = path

        pygame.camera.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        go_fullscreen()

        # Try displaying USB camera view
        self.usb_camera = False
        try:
            self.cam = pygame.camera.Camera("/dev/video0",
                                            (screen_width, screen_height))
            self.cam.start()
            self.usb_camera = True
        except BaseException as camera_exception:
            logging.exception("Open camera: %s", camera_exception)

        self.button_exit = Button(self.screen,
                                  (screen_width - 200, 0, 200, 200),
                                  "images/icons/StopButton.png",
                                  (0, 0, 0))

        self.re_init()

    def update_camera(self):
        """ re draw image from camera """
        if self.usb_camera:
            image = self.cam.get_image()
            image_height = image.get_height()
            self.screen.blit(image,
                             (0, self.screen_size['height'] - image_height))
            pygame.display.update()

        self.re_init()

    def check_exit(self, pos):
        """ check if user has clicked exit button """
        if self.button_exit.check_click(pos):
            self.cam.stop()
            return True
        return False

    def re_init(self):
        """ get pictures from the networked cams """
        try:
            self.image = pygame.image.load("%s/CAMERA1.jpg" % (self.path)).convert()
            self.screen.blit(self.image, (0, 0))
            image_width = self.image.get_width()
            image_height = self.image.get_height()
            try:
                self.image = pygame.image.load("%s/CAMERA2.jpg" % (self.path)).convert()
                self.screen.blit(self.image,
                                 (self.screen_size['width'] - image_width,
                                  self.screen_size['height'] - image_height))
            except BaseException:
                pass
        except BaseException:
            pass
