#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from ctime_common import shuffle_list, play_let_it_go

class TestCtimeCommon(unittest.TestCase):
    
    @patch('ctime_common.random.randint')
    def test_shuffle_list(self, mock_randint):
        mock_randint.side_effect = [0, 2, 2]  # Revised to mimic the "self-swapping" scenario
        original_list = [1, 2, 3]
        shuffled_list = shuffle_list(original_list)
        self.assertEqual(shuffled_list, [1, 3, 2])  # Adjusted expected result

    @patch('ctime_common.pygame')
    def test_play_let_it_go(self, mock_pygame):
        play_let_it_go()
        mock_pygame.mixer.music.load.assert_called_with("tunes/frozen/005.ogg")
        mock_pygame.mixer.music.play.assert_called_once()


if __name__ == '__main__':
    unittest.main()

