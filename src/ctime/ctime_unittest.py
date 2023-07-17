import os
import unittest
import pygame
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pytz
import yaml
from src.ctime.ctime_play_list import PlayListScreen
from src.ctime.ctime_play_list import TrackListScreen
from src.ctime.ctime_camera import Camera
from src.ctime.ctime_common import go_fullscreen
from src.ctime.ctime_facebook import CtimeFacebook
from cmreslogging.handlers import CMRESHandler
import time

class CtimeTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    @unittest.skipIf(os.environ.get('DISPLAY') is None, "No display available")
    def test_play_list_screen(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600
        log = MagicMock()

        # Create an instance of PlayListScreen
        play_list_screen = PlayListScreen(screen_width, screen_height, log)

        # Assert that the instance is created successfully
        self.assertIsInstance(play_list_screen, PlayListScreen)

        # Add additional test cases as needed

    @unittest.skipIf(os.environ.get('DISPLAY') is None, "No display available")
    def test_track_list_screen(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600
        play_list = MagicMock()
        tracks = MagicMock()
        log = MagicMock()

        # Create an instance of TrackListScreen
        track_list_screen = TrackListScreen(screen_width, screen_height, play_list, tracks, log)

        # Assert that the instance is created successfully
        self.assertIsInstance(track_list_screen, TrackListScreen)

        # Add additional test cases as needed

    @unittest.skipIf(os.environ.get('DISPLAY') is None, "No display available")    
    def test_camera(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600
        path = "/path/to/images"
        log = MagicMock()

        # Create an instance of Camera
        camera = Camera(screen_width, screen_height, path, log)

        # Assert that the instance is created successfully
        self.assertIsInstance(camera, Camera)

        # Add additional test cases as needed

    @unittest.skipIf(os.environ.get('DISPLAY') is None, "No display available")    
    def test_main_screen(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Mock pygame methods
        pygame.init = MagicMock()
        pygame.display.set_mode = MagicMock(return_value=MagicMock())
        pygame.display.get_surface().get_width = MagicMock(return_value=screen_width)
        pygame.display.get_surface().get_height = MagicMock(return_value=screen_height)
        pygame.image.load = MagicMock(return_value=MagicMock())

        # Mock other dependencies
        yaml.safe_load = MagicMock(return_value={
            'vol': 0.5,
            'start_time': '10:00:00',
            'end_time': '18:00:00',
            'max_play_length': 3600,
            'power_on': True,
            'power_off': False,
            'facebook_user': 'test_user',
            'facebook_pass': 'test_password',
            'facebook_start': '09:00:00',
            'facebook_end': '19:00:00',
            'facebook_timeout': 10,
            'enable_mouse': True,
            'disable_mouse': False,
            'log_host': 'test_host',
            'log_port': 9200,
            'log_index': 'test_index',
            'pic_loc': '/path/to/pics'
        })
        pygame.mixer.music.set_volume = MagicMock()
        CtimeFacebook = MagicMock()

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        with patch('src.ctime.ctime_common.go_fullscreen'):
            main_screen = MainScreen(screen_width, screen_height)

        # Test the re_init method
        main_screen.re_init()

        # Assert that the screen is re-initialized correctly
        self.assertEqual(main_screen.game_state, 0)
        go_fullscreen.assert_called()
        self.screen.fill.assert_called_with((0, 0, 0))
        self.screen.blit.assert_called_with(main_screen.image, (
            max(0, (main_screen.screen_width - main_screen.image.get_rect().size[0]) / 2),
            max(0, (main_screen.screen_height - main_screen.image.get_rect().size[1]) / 2)
        ))
        self.assertEqual(main_screen.play_state, 1)
        self.button_play.assert_called_with(main_screen.screen, (0, 0, 200, 200), "PLAY_BUTTON", (0, 0, 0), "Play", main_screen.log)
        self.button_play_list.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, 0, 200, 200), "image_list", (0, 0, 0), "PlayList", main_screen.log)
        if is_video_camera_present():
            self.button_video.assert_called_with(main_screen.screen, (0, main_screen.screen_height - 200, 200, 200), "images/icons/VideoButton.png", (0, 0, 0), "Camera", main_screen.log)
        else:
            print.assert_called_with("DEBUG: no video")
            self.assertIsNone(main_screen.button_video)
        self.button_power.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, main_screen.screen_height - 200, 200, 200), "images/icons/light.png", (0, 0, 0), main_screen.power_on, main_screen.power_off, main_screen.log)
        self.button_pairs.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, (main_screen.screen_height / 2) - 100, 200, 200), "images/icons/pairs.png", (0, 0, 0), "Pairs", main_screen.log)

        # Test can_we_facebook method
        main_screen.log = MagicMock()
        main_screen.facebook = True
        main_screen.facebook_user = "test_user"
        main_screen.facebook_pass = "test_password"
        main_screen.facebook_start = "09:00:00"
        main_screen.facebook_end = "19:00:00"
        main_screen.facebook_timeout = 10
        main_screen.facebook_exit = time.time()

        # Test case: all config settings are available
        self.assertTrue(main_screen.can_we_facebook())
        main_screen.log.info.assert_not_called()

        # Test case: video camera not present
        main_screen.facebook = True
        main_screen.facebook_user = "test_user"
        main_screen.facebook_pass = "test_password"
        main_screen.facebook_start = "09:00:00"
        main_screen.facebook_end = "19:00:00"
        main_screen.facebook_timeout = 10
        main_screen.facebook_exit = time.time()
        is_video_camera_present.return_value = False
        self.assertFalse(main_screen.can_we_facebook())
        main_screen.log.info.assert_called_with("no video device, no facebook")

    def test_can_we_play(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Mock pygame methods
        pygame.init = MagicMock()
        pygame.display.set_mode = MagicMock(return_value=MagicMock())
        pygame.display.get_surface().get_width = MagicMock(return_value=screen_width)
        pygame.display.get_surface().get_height = MagicMock(return_value=screen_height)
        pygame.image.load = MagicMock(return_value=MagicMock())

        # Mock other dependencies
        yaml.safe_load = MagicMock(return_value={
            'vol': 0.5,
            'start_time': '10:00:00',
            'end_time': '18:00:00',
            'max_play_length': 3600,
            'power_on': True,
            'power_off': False,
            'facebook_user': 'test_user',
            'facebook_pass': 'test_password',
            'facebook_start': '09:00:00',
            'facebook_end': '19:00:00',
            'facebook_timeout': 10,
            'enable_mouse': True,
            'disable_mouse': False,
            'log_host': 'test_host',
            'log_port': 9200,
            'log_index': 'test_index',
            'pic_loc': '/path/to/pics'
        })
        pygame.mixer.music.set_volume = MagicMock()
        CtimeFacebook = MagicMock()

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        with patch('src.ctime.ctime_common.go_fullscreen'):
            main_screen = MainScreen(screen_width, screen_height)

        # Test can_we_play method
        main_screen.start_time = '10:00:00'
        main_screen.end_time = '18:00:00'

        # Test case: current time is within the start and end time
        now_time = datetime(2023, 7, 17, 12, 0, 0)
        with patch('src.ctime.ctime.datetime') as mock_datetime:
            mock_datetime.now.return_value = now_time
            self.assertTrue(main_screen.can_we_play())

        # Test case: current time is before the start time
        now_time = datetime(2023, 7, 17, 9, 0, 0)
        with patch('src.ctime.ctime.datetime') as mock_datetime:
            mock_datetime.now.return_value = now_time
            self.assertFalse(main_screen.can_we_play())

        # Test case: current time is after the end time
        now_time = datetime(2023, 7, 17, 20, 0, 0)
        with patch('src.ctime.ctime.datetime') as mock_datetime:
            mock_datetime.now.return_value = now_time
            self.assertFalse(main_screen.can_we_play())

    def test_click_button_play(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Mock pygame methods
        pygame.init = MagicMock()
        pygame.display.set_mode = MagicMock(return_value=MagicMock())
        pygame.display.get_surface().get_width = MagicMock(return_value=screen_width)
        pygame.display.get_surface().get_height = MagicMock(return_value=screen_height)
        pygame.image.load = MagicMock(return_value=MagicMock())

        # Mock other dependencies
        yaml.safe_load = MagicMock(return_value={
            'vol': 0.5,
            'start_time': '10:00:00',
            'end_time': '18:00:00',
            'max_play_length': 3600,
            'power_on': True,
            'power_off': False,
            'facebook_user': 'test_user',
            'facebook_pass': 'test_password',
            'facebook_start': '09:00:00',
            'facebook_end': '19:00:00',
            'facebook_timeout': 10,
            'enable_mouse': True,
            'disable_mouse': False,
            'log_host': 'test_host',
            'log_port': 9200,
            'log_index': 'test_index',
            'pic_loc': '/path/to/pics'
        })
        pygame.mixer.music.set_volume = MagicMock()
        CtimeFacebook = MagicMock()

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        with patch('src.ctime.ctime_common.go_fullscreen'):
            main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.can_we_play = MagicMock(return_value=True)
        main_screen.button_play = MagicMock()
        main_screen.play_state = 1
        main_screen.first_play = 1
        main_screen.log = MagicMock()

        # Test case: play_state = 1
        main_screen.click_button_play()
        pygame.mixer.music.pause.assert_called_once()
        main_screen.button_play.change_image.assert_called_with(PLAY_BUTTON)

        # Test case: play_state = 1 and first_play = 1
        main_screen.play_state = 1
        main_screen.first_play = 1
        main_screen.playlist = 0
        main_screen.tune_no = 1
        main_screen.click_button_play()
        pygame.mixer.init.assert_called_once()
        pygame.mixer.music.load.assert_called_with("tunes/bob/001.ogg")
        pygame.mixer.music.play.assert_called_once()
        main_screen.button_play.change_image.assert_called_with(STOP_BUTTON)
        self.assertEqual(main_screen.first_play, 0)
        self.assertEqual(main_screen.play_start, datetime.now(pytz.timezone(CTIME_TIMEZONE)))

        # Test case: play_state = 2
        main_screen.play_state = 2
        main_screen.click_button_play()
        pygame.mixer.music.unpause.assert_called_once()
        main_screen.button_play.change_image.assert_called_with(STOP_BUTTON)
        self.assertEqual(main_screen.play_start, datetime.now(pytz.timezone(CTIME_TIMEZONE)))

    def test_play_next(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Mock pygame methods
        pygame.init = MagicMock()
        pygame.display.set_mode = MagicMock(return_value=MagicMock())
        pygame.display.get_surface().get_width = MagicMock(return_value=screen_width)
        pygame.display.get_surface().get_height = MagicMock(return_value=screen_height)
        pygame.image.load = MagicMock(return_value=MagicMock())

        # Mock other dependencies
        yaml.safe_load = MagicMock(return_value={
            'vol': 0.5,
            'start_time': '10:00:00',
            'end_time': '18:00:00',
            'max_play_length': 3600,
            'power_on': True,
            'power_off': False,
            'facebook_user': 'test_user',
            'facebook_pass': 'test_password',
            'facebook_start': '09:00:00',
            'facebook_end': '19:00:00',
            'facebook_timeout': 10,
            'enable_mouse': True,
            'disable_mouse': False,
            'log_host': 'test_host',
            'log_port': 9200,
            'log_index': 'test_index',
            'pic_loc': '/path/to/pics'
        })
        pygame.mixer.music.set_volume = MagicMock()
        CtimeFacebook = MagicMock()

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        with patch('src.ctime.ctime_common.go_fullscreen'):
            main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.can_we_play = MagicMock(return_value=True)
        main_screen.play_start = datetime.now(pytz.timezone(CTIME_TIMEZONE))
        main_screen.max_play_length = 60
        main_screen.play_state = 0
        main_screen.game_state = 0
        main_screen.button_play = MagicMock()
        main_screen.playlist = 0
        main_screen.tune_no = 1
        main_screen.play_len = {0: 3, 1: 3, 2: 3}
        pygame.mixer.music.load = MagicMock()
        pygame.mixer.music.play = MagicMock()

        # Test case: can_we_play returns False
        main_screen.can_we_play.return_value = False
        main_screen.play_next()
        main_screen.button_play.change_image.assert_not_called()
        pygame.mixer.music.load.assert_not_called()
        pygame.mixer.music.play.assert_not_called()

        # Test case: current play time exceeds max play length
        main_screen.can_we_play.return_value = True
        main_screen.play_start = datetime.now(pytz.timezone(CTIME_TIMEZONE)) - timedelta(minutes=61)
        main_screen.play_next()
        self.assertEqual(main_screen.play_state, 1)
        if main_screen.game_state == 0:
            main_screen.button_play.change_image.assert_called_with(PLAY_BUTTON)
        pygame.mixer.music.load.assert_not_called()
        pygame.mixer.music.play.assert_not_called()

        # Test case: regular play next
        main_screen.play_state = 0
        main_screen.game_state = 0
        main_screen.tune_no = 2
        main_screen.play_next()
        self.assertEqual(main_screen.tune_no, 3)
        self.assertEqual(main_screen.playlist, 0)
        pygame.mixer.music.load.assert_called_with("tunes/bob/003.ogg")
        pygame.mixer.music.play.assert_called_once()

        # Test case: playlist 1
        main_screen.playlist = 1
        main_screen.play_next()
        self.assertEqual(main_screen.tune_no, 1)
        self.assertEqual(main_screen.playlist, 1)
        pygame.mixer.music.load.assert_called_with("tunes/frozen/001.ogg")
        pygame.mixer.music.play.assert_called_once()

        # Test case: playlist 2
        main_screen.playlist = 2
        main_screen.play_next()
        self.assertEqual(main_screen.tune_no, 2)
        self.assertEqual(main_screen.playlist, 2)
        pygame.mixer.music.load.assert_called_with("tunes/showman/002.ogg")
        pygame.mixer.music.play.assert_called_once()

    def test_click_button_video(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Create an instance of MainScreen
        main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.log = MagicMock()
        main_screen.screen_width = screen_width
        main_screen.screen_height = screen_height
        main_screen.path = "/path/to/images"

        # Mock the Camera class
        Camera = MagicMock()

        # Call the click_button_video method
        main_screen.click_button_video()

        # Verify the method calls
        main_screen.log.info.assert_called_with('start video show')
        Camera.assert_called_with(screen_width, screen_height, "/path/to/images", main_screen.log)

if __name__ == '__main__':
    unittest.main()

