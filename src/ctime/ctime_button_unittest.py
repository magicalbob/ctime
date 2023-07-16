#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
import time
from src.ctime.ctime_button import Button

class TestButton(unittest.TestCase):

    @patch('pygame.image.load')
    def setUp(self, mock_image_load):
        self.screen = Mock()
        self.rect = (0, 0, 100, 50)
        self.image_path = 'button.png'
        self.colorkey = (255, 255, 255)
        self.log = Mock()

        # Mock the image and its methods
        self.mock_image = Mock()
        self.mock_image.convert.return_value = self.mock_image
        mock_image_load.return_value = self.mock_image

        self.button = Button(self.screen, self.rect, self.image_path, self.colorkey, 'TestButton', self.log)
        # Reset the call count for 'blit' after the Button object is created
        self.screen.reset_mock()

    def test_init(self):
        self.assertEqual(self.button.name, 'TestButton')
        self.assertEqual(self.button.rect, self.rect)
        self.assertIsNotNone(self.button.image)

    @patch('pygame.image.load')
    def test_redraw(self, mock_image_load):
        self.button.redraw()
        self.screen.blit.assert_called_once()

    @patch('pygame.image.load')
    def test_reload(self, mock_image_load):
        self.button.reload(self.image_path)
        self.screen.blit.assert_called_once()

    @patch('pygame.image.load')
    def test_change_image(self, mock_image_load):
        new_image_path = 'new_button.png'
        self.button.change_image(new_image_path)
        mock_image_load.assert_called_with(new_image_path)
        self.screen.blit.assert_called_once()

    def test_check_click(self):
        # Delay more than a second to account for the rate limit on check_click
        time.sleep(2)
        pos_inside = (25, 25)
        self.assertTrue(self.button.check_click(pos_inside))
        time.sleep(2)
        pos_outside = (200, 200) 
        self.assertFalse(self.button.check_click(pos_outside))

if __name__ == '__main__':
    unittest.main()
