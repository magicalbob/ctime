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

PATH_TO_IMAGES = "./images/backgrounds/"
DATETIME_MODULE = 'src.ctime.ctime.datetime'

class CtimeTestCase(unittest.TestCase):
    def setUp(self):
        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen
        self.main_screen = MainScreen(800, 600)
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

    @unittest.skipIf(os.environ.get('DISPLAY') is None, "No display available")
    def test_camera(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600
        path = PATH_TO_IMAGES
        log = MagicMock()

        # Create an instance of Camera
        camera = Camera(screen_width, screen_height, path, log)

        # Assert that the instance is created successfully
        self.assertIsInstance(camera, Camera)

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
        with patch(DATETIME_MODULE) as mock_datetime:
            mock_datetime.now.return_value = now_time
            self.assertTrue(main_screen.can_we_play())

        # Test case: current time is before the start time
        now_time = datetime(2023, 7, 17, 9, 0, 0)
        with patch(DATETIME_MODULE) as mock_datetime:
            mock_datetime.now.return_value = now_time
            self.assertFalse(main_screen.can_we_play())

        # Test case: current time is after the end time
        now_time = datetime(2023, 7, 17, 20, 0, 0)
        with patch(DATETIME_MODULE) as mock_datetime:
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
        with patch('src.ctime.ctime_common.go_fullscreen'), \
                patch('pygame.FULLSCREEN', 0), \
                patch('pygame.HWSURFACE', 0), \
                patch('pygame.DOUBLEBUF', 0):
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

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

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

    def test_click_play_list(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.log = MagicMock()
        main_screen.screen_width = screen_width
        main_screen.screen_height = screen_height

        # Mock the PlayListScreen class
        play_list_screen = MagicMock()

        # Call the click_play_list method
        main_screen.click_play_list()

        # Verify the method calls
        play_list_screen.assert_called_with(screen_width, screen_height, main_screen.log)

    def test_click_button_power(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.log = MagicMock()
        main_screen.screen_width = screen_width
        main_screen.screen_height = screen_height
        main_screen.power_on = True
        main_screen.power_off = False

        # Call the click_button_power method
        main_screen.click_button_power()

        # Verify the method calls
        main_screen.log.info.assert_called_with('power: %s' % (not main_screen.power_on))

        # Test case: power_on is True
        main_screen.click_button_power()
        main_screen.log.info.assert_called_with('power: %s' % main_screen.power_on)

    def test_click_button_pairs(self):
        # Mock necessary dependencies
        screen_width = 800
        screen_height = 600

        # Import MainScreen after mocking dependencies
        from src.ctime.ctime import MainScreen

        # Create an instance of MainScreen
        main_screen = MainScreen(screen_width, screen_height)

        # Set up initial state
        main_screen.log = MagicMock()
        main_screen.screen_width = screen_width
        main_screen.screen_height = screen_height

        # Mock the TrackListScreen class
        TrackListScreen = MagicMock()

        # Call the click_button_pairs method
        main_screen.click_button_pairs()

        # Verify the method calls
        TrackListScreen.assert_called_with(screen_width, screen_height, main_screen.playlist, main_screen.tracks, main_screen.log)

    def test_play_track(self):
        # Mock necessary dependencies
        log = MagicMock()
        play_list = 0
        tune_no = 1
        pygame.mixer.music.load = MagicMock()
        pygame.mixer.music.play = MagicMock()
        refresh_pic = MagicMock()
        button_play_change_image = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)

        # Call the play_track method
        main_screen.play_track(play_list, tune_no)

        # Verify the method calls and assertions
        log.info.assert_called_with('play some music')
        pygame.mixer.music.load.assert_called_with('tunes/bob/001.ogg')
        pygame.mixer.music.play.assert_called_once()
        refresh_pic.assert_called_once()
        button_play_change_image.assert_called_with(STOP_BUTTON)
        self.assertEqual(main_screen.first_play, 0)
        self.assertEqual(main_screen.game_state, 0)
        self.assertEqual(main_screen.play_state, 2)

    def test_event_state_0(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        button_play = MagicMock()
        button_video = MagicMock()
        button_play_list = MagicMock()
        button_power = MagicMock()
        button_pairs = MagicMock()
        button_facebook = MagicMock()
        click_button_play = MagicMock()
        click_button_video = MagicMock()
        click_play_list = MagicMock()
        refresh_pic = MagicMock()
        click_pairs = MagicMock()
        click_facebook = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)
        main_screen.button_play = button_play
        main_screen.button_video = button_video
        main_screen.button_play_list = button_play_list
        main_screen.button_power = button_power
        main_screen.button_pairs = button_pairs
        main_screen.button_facebook = button_facebook
        main_screen.click_button_play = click_button_play
        main_screen.click_button_video = click_button_video
        main_screen.click_play_list = click_play_list
        main_screen.refresh_pic = refresh_pic
        main_screen.click_pairs = click_pairs
        main_screen.click_facebook = click_facebook

        # Test case: button_play.check_click returns True
        button_play.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_play clicked')
        click_button_play.assert_called_once()
        button_video.check_click.assert_not_called()
        button_play_list.check_click.assert_not_called()
        button_power.check_click.assert_not_called()
        button_pairs.check_click.assert_not_called()
        button_facebook.check_click.assert_not_called()

        # Test case: button_video is not None and button_video.check_click returns True
        button_play.check_click.return_value = False
        button_video.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_video clicked')
        click_button_video.assert_called_once()
        button_play_list.check_click.assert_not_called()
        button_power.check_click.assert_not_called()
        button_pairs.check_click.assert_not_called()
        button_facebook.check_click.assert_not_called()

        # Test case: button_play_list.check_click returns True
        button_video.check_click.return_value = False
        button_play_list.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_play_list clicked')
        click_play_list.assert_called_once()
        button_power.check_click.assert_not_called()
        button_pairs.check_click.assert_not_called()
        button_facebook.check_click.assert_not_called()

        # Test case: button_power.check_click returns True
        button_play_list.check_click.return_value = False
        button_power.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_power clicked')
        refresh_pic.assert_called_once()
        button_pairs.check_click.assert_not_called()
        button_facebook.check_click.assert_not_called()

        # Test case: button_pairs.check_click returns True
        button_power.check_click.return_value = False
        button_pairs.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_pairs clicked')
        click_pairs.assert_called_once()
        button_facebook.check_click.assert_not_called()

        # Test case: button_facebook is not None and button_facebook.check_click returns True
        button_pairs.check_click.return_value = False
        button_facebook.check_click.return_value = True
        main_screen.event_state_0(coord)
        log.info.assert_called_with('button_facebook clicked')
        self.assertIsNone(main_screen.button_facebook)
        refresh_pic.assert_called_once()
        click_facebook.assert_called_once()

    def test_event_state_2(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        video_screen = MagicMock()
        refresh_pic = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)
        main_screen.video_screen = video_screen
        main_screen.refresh_pic = refresh_pic

        # Test case: self.video_screen.check_exit returns True
        video_screen.check_exit.return_value = True
        main_screen.event_state_2(coord)
        self.assertEqual(main_screen.game_state, 0)
        refresh_pic.assert_called_once()

        # Test case: self.video_screen.check_exit returns False
        video_screen.check_exit.return_value = False
        main_screen.event_state_2(coord)
        self.assertIsNone(main_screen.game_state)
        refresh_pic.assert_not_called()

    def test_event_state_3(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        play_list = MagicMock()
        track_list_screen = MagicMock()
        refresh_pic = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)
        main_screen.play_list = play_list
        main_screen.track_list = track_list_screen
        main_screen.refresh_pic = refresh_pic

        # Test case: play_list.check_click_bob returns True
        play_list.check_click_bob.return_value = True
        main_screen.event_state_3(coord)
        self.assertEqual(main_screen.game_state, 4)
        self.assertEqual(main_screen.playlist, 0)
        track_list_screen.assert_called_with(main_screen.screen_width, main_screen.screen_height, "bob", main_screen.play_len[0], log)
        refresh_pic.assert_called_once()

        # Test case: play_list.check_click_frozen returns True
        play_list.check_click_bob.return_value = False
        play_list.check_click_frozen.return_value = True
        main_screen.event_state_3(coord)
        self.assertEqual(main_screen.game_state, 4)
        self.assertEqual(main_screen.playlist, 1)
        track_list_screen.assert_called_with(main_screen.screen_width, main_screen.screen_height, "frozen", main_screen.play_len[1], log)
        refresh_pic.assert_called_once()

        # Test case: play_list.check_click_showman returns True
        play_list.check_click_frozen.return_value = False
        play_list.check_click_showman.return_value = True
        main_screen.event_state_3(coord)
        self.assertEqual(main_screen.game_state, 4)
        self.assertEqual(main_screen.playlist, 2)
        track_list_screen.assert_called_with(main_screen.screen_width, main_screen.screen_height, "showman", main_screen.play_len[2], log)
        refresh_pic.assert_called_once()

        # Test case: play_list.check_exit returns True
        play_list.check_click_showman.return_value = False
        play_list.check_exit.return_value = True
        main_screen.event_state_3(coord)
        self.assertEqual(main_screen.game_state, 0)
        refresh_pic.assert_called_once()

    def test_event_state_4(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        track_list = MagicMock()
        click_pairs = MagicMock()
        play_track = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)
        main_screen.track_list = track_list
        main_screen.click_pairs = click_pairs
        main_screen.play_track = play_track

        # Test case: is_clicked is True and playlist is 1 and track_no is 5
        track_list.check_click.return_value = (5, True)
        main_screen.playlist = 1
        main_screen.event_state_4(coord)
        click_pairs.assert_called_once()
        play_track.assert_not_called()

        # Test case: is_clicked is True and playlist is not 1 or track_no is not 5
        track_list.check_click.return_value = (2, True)
        main_screen.playlist = 0
        main_screen.event_state_4(coord)
        play_track.assert_called_with(0, 2)
        click_pairs.assert_not_called()

        # Test case: is_clicked is False
        track_list.check_click.return_value = (3, False)
        main_screen.event_state_4(coord)
        play_track.assert_not_called()
        click_pairs.assert_not_called()

    def test_event_state_5(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        pairs = MagicMock()
        refresh_pic = MagicMock()

        # Create an instance of MainScreen
        main_screen = MainScreen(log=log)
        main_screen.pairs = pairs
        main_screen.refresh_pic = refresh_pic

        # Test case: pair_state is -2
        pairs.check_click.return_value = (-2, None)
        main_screen.event_state_5(coord)
        self.assertEqual(main_screen.game_state, 0)
        refresh_pic.assert_called_once()

        # Test case: pair_state is not -2
        pairs.check_click.return_value = (0, None)
        main_screen.event_state_5(coord)
        refresh_pic.assert_not_called()

    def test_check_event(self):
        # Mock necessary dependencies
        coord = (100, 100)
        log = MagicMock()
        main_screen = MainScreen(screen_width=800, screen_height=600)
        main_screen.event_state_0 = MagicMock()
        main_screen.event_state_2 = MagicMock()
        main_screen.event_state_3 = MagicMock()
        main_screen.event_state_4 = MagicMock()
        main_screen.event_state_5 = MagicMock()

        # Test case: event.type is pygame.MOUSEBUTTONUP
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONUP
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_not_called()
        main_screen.event_state_2.assert_not_called()
        main_screen.event_state_3.assert_not_called()
        main_screen.event_state_4.assert_not_called()
        main_screen.event_state_5.assert_not_called()

        # Test case: game_state is 0
        main_screen.game_state = 0
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_called_with(coord)
        main_screen.event_state_2.assert_not_called()
        main_screen.event_state_3.assert_not_called()
        main_screen.event_state_4.assert_not_called()
        main_screen.event_state_5.assert_not_called()

        # Test case: game_state is 2
        main_screen.game_state = 2
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_not_called()
        main_screen.event_state_2.assert_called_with(coord)
        main_screen.event_state_3.assert_not_called()
        main_screen.event_state_4.assert_not_called()
        main_screen.event_state_5.assert_not_called()

        # Test case: game_state is 3
        main_screen.game_state = 3
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_not_called()
        main_screen.event_state_2.assert_not_called()
        main_screen.event_state_3.assert_called_with(coord)
        main_screen.event_state_4.assert_not_called()
        main_screen.event_state_5.assert_not_called()

        # Test case: game_state is 4
        main_screen.game_state = 4
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_not_called()
        main_screen.event_state_2.assert_not_called()
        main_screen.event_state_3.assert_not_called()
        main_screen.event_state_4.assert_called_with(coord)
        main_screen.event_state_5.assert_not_called()

        # Test case: game_state is 5
        main_screen.game_state = 5
        main_screen.check_event(event, coord)
        main_screen.event_state_0.assert_not_called()
        main_screen.event_state_2.assert_not_called()
        main_screen.event_state_3.assert_not_called()
        main_screen.event_state_4.assert_not_called()
        main_screen.event_state_5.assert_called_with(coord)

    def test_refresh_pic(self):
        # Test that the method properly redraws the background picture
        self.main_screen.refresh_pic()

        # Add your assertions here to verify the expected behavior
        # For example, you can assert that the image is loaded correctly:
        self.assertIsNotNone(self.main_screen.image)

        # Assert other expectations based on your specific implementation

        # Verify that the necessary buttons are redrawn
        self.assertIsNotNone(self.main_screen.button_play)
        self.assertIsNotNone(self.main_screen.button_play_list)
        self.assertIsNotNone(self.main_screen.button_power)
        self.assertIsNotNone(self.main_screen.button_pairs)

        # If the button_video is None, assert that it remains None after the method call
        self.assertIsNone(self.main_screen.button_video)

        # If can_we_facebook() returns True, assert the creation or redraw of button_facebook
        if self.main_screen.can_we_facebook():
            self.assertIsNotNone(self.main_screen.button_facebook)

    def test_update_pic_with_image_files(self):
        # Test when there are image files in the background directory
        image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg']

        # Save the original back_no value
        original_back_no = self.main_screen.back_no

        # Mock the os.listdir function to return the image files
        with unittest.mock.patch('os.listdir', return_value=image_files):
            self.main_screen.update_pic()

        # Assert that back_no has been incremented and wrapped correctly
        self.assertEqual(self.main_screen.back_no, original_back_no + 1 if original_back_no < len(image_files) else 1)

        # Assert that refresh_pic is called after updating the picture
        self.assertTrue(self.main_screen.refresh_pic_called)

        # Add more assertions as needed to cover the behavior of the method

    def test_update_pic_without_image_files(self):
        # Test when there are no image files in the background directory
        image_files = []

        # Save the original back_no value
        original_back_no = self.main_screen.back_no

        # Mock the os.listdir function to return the image files
        with unittest.mock.patch('os.listdir', return_value=image_files):
            self.main_screen.update_pic()

        # Assert that back_no remains unchanged
        self.assertEqual(self.main_screen.back_no, original_back_no)

        # Assert that refresh_pic is not called
        self.assertFalse(self.main_screen.refresh_pic_called)

        # Add more assertions as needed to cover the behavior of the method


if __name__ == '__main__':
    unittest.main()
