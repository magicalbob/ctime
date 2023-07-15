#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
from src.ctime.ctime_blank import BlankScreen

class TestBlankScreen(unittest.TestCase):

    @patch('src.ctime.ctime_blank.pygame')
    @patch('src.ctime.ctime_blank.go_fullscreen')
    def test_BlankScreen(self, mock_go_fullscreen, mock_pygame):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_ctime.button_power.rpi_power = MagicMock()

        mock_log = MagicMock()

        mock_display = MagicMock()
        mock_pygame.display.get_surface.return_value = mock_display

        # Initialize the class
        blank_screen = BlankScreen(mock_ctime, 800, 600, mock_log)

        # Assertions to verify that calls have been made correctly
        mock_log.info.assert_any_call('Time for bed said Zeberdee')
        mock_log.info.assert_any_call('Lights out')

        mock_display.fill.assert_called_once_with(mock_pygame.Color(0, 0, 0, 0),
                                                  (0, 0, 800, 600), 0)
        mock_ctime.button_power.rpi_power.assert_called_once()
        mock_go_fullscreen.assert_called_once()

if __name__ == '__main__':
    unittest.main()
