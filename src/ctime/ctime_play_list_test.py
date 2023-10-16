import unittest
from unittest.mock import Mock, patch
import pygame
from ctime_play_list import TrackListScreen, PlayListScreen

class TestTrackListScreen(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.play_list = "test_play_list"
        self.tracks = 10
        self.log = Mock()

        self.screen = Mock()
        self.screen.fill = Mock()

        pygame.display.get_surface = Mock(return_value=self.screen)

        with patch("src.ctime.ctime_play_list.go_fullscreen"):
            self.track_list_screen = TrackListScreen(self.screen_width, self.screen_height, self.play_list, self.tracks, self.log)
            self.track_list_screen.screen = self.screen

    def test_get_button_pos(self):
        button_pos = self.track_list_screen.get_button_pos(0)
        self.assertEqual(button_pos, [-44.44444444444444, 0.0])

    def test_check_click(self):
        pos = (100, 100)
        result = self.track_list_screen.check_click(pos)
        self.assertEqual(result, [-1, False])

    def test_check_click_track(self):
        # Create a mock button instance
        mock_button = Mock()
        mock_button.check_click.return_value = True

        # Replace a button in the list with the mock button
        self.track_list_screen.track_list[0] = mock_button

        pos = (100, 100)
        result = self.track_list_screen.check_click(pos)

        # Check that the result indicates a track was clicked
        self.assertEqual(result, [1, True])

class TestPlayListScreen(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.log = Mock()

        self.screen = Mock()
        self.screen.fill = Mock()

        pygame.display.get_surface = Mock(return_value=self.screen)

        with patch("src.ctime.ctime_play_list.go_fullscreen"):
            self.play_list_screen = PlayListScreen(self.screen_width, self.screen_height, self.log)
            self.play_list_screen.screen = self.screen

    def test_check_click_bob(self):
        pos = (100, 100)
        result = self.play_list_screen.check_click_bob(pos)
        self.assertFalse(result)

    def test_check_click_frozen(self):
        pos = (100, 100)
        result = self.play_list_screen.check_click_frozen(pos)
        self.assertFalse(result)

    def test_check_click_showman(self):
        pos = (100, 100)
        result = self.play_list_screen.check_click_showman(pos)
        self.assertFalse(result)

    def test_check_exit(self):
        pos = (100, 100)
        result = self.play_list_screen.check_exit(pos)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

