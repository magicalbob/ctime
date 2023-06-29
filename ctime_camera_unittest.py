#!/usr/bin/env python3
import unittest
import pygame
from unittest.mock import MagicMock, patch
from camera import Camera

class TestCamera(unittest.TestCase):
    @patch('pygame.camera.Camera')
    @patch('pygame.camera.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.update')
    @patch('pygame.image.load')
    def test_update_camera_with_usb_camera(self, mock_load, mock_update, mock_set_mode, mock_init, mock_camera):
        screen_width = 800
        screen_height = 600
        camera_instance = mock_camera.return_value
        mock_cam = MagicMock()
        mock_cam.get_image.return_value = pygame.Surface((screen_width, screen_height))
        camera_instance.start.return_value = mock_cam

        camera = Camera(screen_width, screen_height, "path", MagicMock())
        camera.update_camera()

        mock_cam.get_image.assert_called_once()
        mock_update.assert_called_once()

    @patch('pygame.camera.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.update')
    @patch('pygame.image.load')
    def test_update_camera_without_usb_camera(self, mock_load, mock_update, mock_set_mode, mock_init):
        screen_width = 800
        screen_height = 600

        camera = Camera(screen_width, screen_height, "path", MagicMock())
        camera.update_camera()

        mock_update.assert_not_called()

    @patch('pygame.camera.Camera')
    @patch('pygame.camera.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.update')
    @patch('pygame.image.load')
    def test_check_exit_with_button_click(self, mock_load, mock_update, mock_set_mode, mock_init, mock_camera):
        screen_width = 800
        screen_height = 600
        camera_instance = mock_camera.return_value
        mock_cam = MagicMock()
        camera_instance.start.return_value = mock_cam
        camera = Camera(screen_width, screen_height, "path", MagicMock())

        pos = (screen_width - 100, 100)
        self.assertTrue(camera.check_exit(pos))
        mock_cam.stop.assert_called_once()

    @patch('pygame.camera.Camera')
    @patch('pygame.camera.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.update')
    @patch('pygame.image.load')
    def test_check_exit_without_button_click(self, mock_load, mock_update, mock_set_mode, mock_init, mock_camera):
        screen_width = 800
        screen_height = 600
        camera_instance = mock_camera.return_value
        mock_cam = MagicMock()
        camera_instance.start.return_value = mock_cam
        camera = Camera(screen_width, screen_height, "path", MagicMock())

        pos = (100, 100)
        self.assertFalse(camera.check_exit(pos))
        mock_cam.stop.assert_not_called()

if __name__ == '__main__':
    unittest.main()

