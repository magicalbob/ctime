import unittest
from unittest.mock import patch, MagicMock
import pygame
from ctime_pairs import PairsScreen

class TestPairsScreen(unittest.TestCase):

    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600
        self.ctime_mock = MagicMock()
        self.pairs_screen = PairsScreen(self.screen_width, self.screen_height, self.ctime_mock)

    @patch('ctime_pairs.Button')
    @patch('ctime_pairs.shuffle_list')
    def test_init(self, mock_shuffle_list, mock_button):
        mock_shuffle_list.return_value = [0, 1, 2, 3, 4, 5, 6, 7]

        pairs_screen = PairsScreen(self.screen_width, self.screen_height, self.ctime_mock)

        self.assertEqual(pairs_screen.screen_size['width'], self.screen_width)
        self.assertEqual(pairs_screen.screen_size['height'], self.screen_height)
        self.assertTrue(mock_shuffle_list.called)
        self.assertEqual(len(pairs_screen.cards['list']), 8)
        self.assertIsNotNone(pairs_screen.log)

    def test_get_button_pos(self):
        pos = self.pairs_screen.get_button_pos(0)
        self.assertEqual(pos, [50, 100])

        pos = self.pairs_screen.get_button_pos(4)
        self.assertEqual(pos, [50, 500])

    @patch('ctime_pairs.time.time')
    def test_flip_back(self, mock_time):
        mock_time.return_value = 10

        self.pairs_screen.cards['clicked'] = [0, 1]
        self.pairs_screen.cards['list'][0].cardDone = False

        self.pairs_screen.flip_back()

        self.assertTrue(self.pairs_screen.cards['list'][0].reload.called)
        self.assertTrue(self.pairs_screen.cards['list'][1].reload.called)

    @patch('ctime_pairs.time.time')
    def test_flip_card(self, mock_time):
        mock_time.return_value = 10

        self.pairs_screen.cards['clicked'] = [-1, -1]
        self.pairs_screen.cards['list'][0].cardDone = False

        self.pairs_screen.flip_card(0)

        self.assertEqual(self.pairs_screen.cards['clicked'][0], 0)
        self.assertTrue(self.pairs_screen.cards['list'][0].reload.called)

    @patch('ctime_pairs.time.time')
    def test_flip_card_already_turned(self, mock_time):
        mock_time.return_value = 10

        self.pairs_screen.cards['clicked'] = [0, -1]
        self.pairs_screen.cards['list'][0].cardDone = True

        self.pairs_screen.flip_card(0)

        self.assertEqual(self.pairs_screen.cards['clicked'][0], 0)
        self.assertFalse(self.pairs_screen.cards['list'][0].reload.called)

    def test_check_click_exit_button(self):
        pos = [self.screen_width - 200, 0]

        with patch.object(self.pairs_screen.button_exit, 'check_click', return_value=True):
            result = self.pairs_screen.check_click(pos)

        self.assertEqual(result, [-2, False])

    def test_check_click_facebook_button(self):
        pos = [self.screen_width - 200, self.screen_height - 200]

        with patch.object(self.pairs_screen.button_facebook, 'check_click', return_value=True):
            with patch.object(self.pairs_screen.ctime, 'can_we_facebook', return_value=True):
                result = self.pairs_screen.check_click(pos)

        self.assertEqual(result, [0, True])
        self.assertIsNone(self.pairs_screen.button_facebook)

    def test_check_click_card_button(self):
        pos = [50, 100]

        result = self.pairs_screen.check_click(pos)

        self.assertEqual(result, [0, True])

    def test_play_success(self):
        with patch.object(self.pairs_screen, 'add_button_exit'):
            with patch.object(self.pairs_screen, 'play_applause'):
                with patch.object(self.pairs_screen, 'redraw'):
                    self.pairs_screen.play_success()

        self.assertTrue(self.pairs_screen.add_button_exit.called)
        self.assertTrue(self.pairs_screen.play_applause.called)
        self.assertTrue(self.pairs_screen.redraw.called)

    @patch('ctime_pairs.pygame.mixer.init')
    @patch('ctime_pairs.pygame.mixer.music.load')
    @patch('ctime_pairs.pygame.mixer.music.play')
    def test_play_applause(self, mock_play, mock_load, mock_init):
        self.pairs_screen.play_applause()

        self.assertTrue(mock_init.called)
        self.assertTrue(mock_load.called)
        self.assertTrue(mock_play.called)

if __name__ == '__main__':
    unittest.main()
