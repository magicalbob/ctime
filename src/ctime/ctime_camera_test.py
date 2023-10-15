import unittest
from unittest.mock import patch, MagicMock
import pygame
from ctime_camera import Camera

class TestCamera(unittest.TestCase):

    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.path = "/path/to/images"
        self.log_mock = MagicMock()
        self.camera = Camera(self.screen_width, self.screen_height, self.path, self.log_mock)

    @patch('ctime_camera.pygame.camera.init')
    @patch('ctime_camera.pygame.display.set_mode')
    @patch('ctime_camera.go_fullscreen')
    def test_init(self, mock_go_fullscreen, mock_set_mode, mock_init):
        mock_set_mode.return_value = self.camera.screen
        mock_camera = MagicMock()
        mock_camera.start.return_value = None
        mock_init.return_value = None

        with patch('ctime_camera.pygame.camera.Camera', return_value=mock_camera):
            camera = Camera(self.screen_width, self.screen_height, self.path, self.log_mock)

        self.assertTrue(mock_init.called)
        self.assertTrue(mock_set_mode.called)
        self.assertTrue(mock_go_fullscreen.called)
        self.assertTrue(mock_camera.start.called)
        self.assertTrue(camera.usb_camera)
        self.assertIsNotNone(camera.button_exit)

    def test_update_camera(self):
        mock_image = MagicMock()
        mock_image.get_height.return_value = 200
        mock_cam = MagicMock()
        mock_cam.get_image.return_value = mock_image
        self.camera.cam = mock_cam

        self.camera.update_camera()

        self.assertTrue(mock_cam.get_image.called)
        self.assertTrue(self.camera.screen.blit.called)
        self.assertTrue(pygame.display.update.called)

    @patch('ctime_camera.pygame.event.get')
    @patch('ctime_camera.pygame.event.Event')
    def test_check_exit(self, mock_event, mock_get):
        mock_event().type = pygame.locals.QUIT
        mock_get.return_value = [mock_event]

        result = self.camera.check_exit((0, 0))

        self.assertTrue(result)
        self.assertTrue(self.camera.cam.stop.called)

    def test_re_init(self):
        mock_image = MagicMock()
        mock_image.get_width.return_value = 200
        mock_image.get_height.return_value = 200
        mock_screen = MagicMock()
        self.camera.image = mock_image
        self.camera.screen = mock_screen

        self.camera.re_init()

        self.assertTrue(pygame.image.load.called)
        self.assertTrue(mock_screen.blit.called)

if __name__ == '__main__':
    unittest.main()
