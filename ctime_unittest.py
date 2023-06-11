#!/usr/bin/env python3
import unittest
import pygame
from unittest.mock import patch, MagicMock

from ctime import MainScreen

class MainScreenTest(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    @patch('ctime.pygame.mixer')
    def test_click_button_play(self, mock_mixer):
        screen_width = 800
        screen_height = 600
        main_screen = MainScreen(screen_width, screen_height)
        main_screen.play_state = 1
        main_screen.first_play = 1
        main_screen.playlist = -1
        main_screen.tune_no = 1

        main_screen.click_button_play()

        self.assertEqual(main_screen.play_state, 2)
        self.assertEqual(main_screen.first_play, 0)
        self.assertEqual(main_screen.game_state, 0)
        self.assertEqual(main_screen.button_play.image_path, "images/icons/StopButton.png")
        mock_mixer.music.load.assert_called_with("tunes/bob/001.ogg")
        mock_mixer.music.play.assert_called()

    @patch('ctime.pygame.mixer')
    def test_play_next(self, mock_mixer):
        screen_width = 800
        screen_height = 600
        main_screen = MainScreen(screen_width, screen_height)
        main_screen.can_we_play = MagicMock(return_value=True)
        main_screen.play_start = MagicMock()
        main_screen.playlist = 0
        main_screen.tune_no = 1
        main_screen.play_len = [10, 32, 11]

        main_screen.play_next()

        self.assertEqual(main_screen.tune_no, 2)
        mock_mixer.music.load.assert_called_with("tunes/bob/002.ogg")
        mock_mixer.music.play.assert_called()

    def test_can_we_play(self):
        screen_width = 800
        screen_height = 600
        main_screen = MainScreen(screen_width, screen_height)
        main_screen.start_time = "08:00:00"
        main_screen.end_time = "18:00:00"

        # Test within the allowed time
        main_screen.get_current_time = MagicMock(return_value="12:00:00")
        self.assertTrue(main_screen.can_we_play())

        # Test outside the allowed time
        main_screen.get_current_time = MagicMock(return_value="20:00:00")
        self.assertFalse(main_screen.can_we_play())

if __name__ == '__main__':
    unittest.main()

