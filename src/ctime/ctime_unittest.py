import unittest
import pygame
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.ctime.ctime_play_list import PlayListScreen
from src.ctime.ctime_play_list import TrackListScreen
from src.ctime.ctime_camera import Camera
from src.ctime.ctime_common import go_fullscreen
from src.ctime.ctime_facebook import CtimeFacebook
from cmreslogging.handlers import CMRESHandler

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

        # Mock datetime methods
        datetime.now = MagicMock(return_value=datetime(2023, 7, 17, 10, 0, 0))
        datetime.datetime.now = MagicMock(return_value=datetime(2023, 7, 17, 10, 0, 0))

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
        self.button_play.assert_called_with(main_screen.screen, (0, 0, 200, 200), PLAY_BUTTON, (0, 0, 0), "Play", main_screen.log)
        self.button_play_list.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, 0, 200, 200), image_list, (0, 0, 0), "PlayList", main_screen.log)
        if is_video_camera_present():
            self.button_video.assert_called_with(main_screen.screen, (0, main_screen.screen_height - 200, 200, 200), "images/icons/VideoButton.png", (0, 0, 0), "Camera", main_screen.log)
        else:
            print.assert_called_with("DEBUG: no video")
            self.assertIsNone(main_screen.button_video)
        self.button_power.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, main_screen.screen_height - 200, 200, 200), "images/icons/light.png", (0, 0, 0), main_screen.power_on, main_screen.power_off, main_screen.log)
        self.button_pairs.assert_called_with(main_screen.screen, (main_screen.screen_width - 200, (main_screen.screen_height / 2) - 100, 200, 200), "images/icons/pairs.png", (0, 0, 0), "Pairs", main_screen.log)
        print.assert_called_with("DEBUG: can we facebook")
        if main_screen.can_we_facebook():
            print.assert_called_with("DEBUG: yes we can")
            self.button_facebook.assert_called_with(main_screen.screen, (0, (main_screen.screen_height / 2) - 100, 200, 200), "images/icons/Phone.png", (0, 0, 0), "Facebook", main_screen.log)
        else:
            print.assert_called_with("DEBUG: no we can't")
            self.assertIsNone(main_screen.button_facebook)

if __name__ == "__main__":
    unittest.main()

