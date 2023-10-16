import unittest
from unittest.mock import Mock, patch
from src.ctime.ctime_common import shuffle_list, play_let_it_go, go_fullscreen, go_minimal, is_video_camera_present

class TestCtimeCommon(unittest.TestCase):
    
    @patch('src.ctime.ctime_common.random.randint')
    def test_shuffle_list(self, mock_randint):
        mock_randint.side_effect = [0, 2, 2]  # Revised to mimic the "self-swapping" scenario
        original_list = [1, 2, 3]
        shuffled_list = shuffle_list(original_list)
        self.assertEqual(shuffled_list, [1, 3, 2])  # Adjusted expected result

    @patch('src.ctime.ctime_common.pygame')
    def test_play_let_it_go(self, mock_pygame):
        play_let_it_go()
        mock_pygame.mixer.init.assert_called_once()
        mock_pygame.mixer.music.load.assert_called_with("tunes/frozen/005.ogg")
        mock_pygame.mixer.music.play.assert_called_once()

    @patch('src.ctime.ctime_common.pygame')
    @patch('src.ctime.ctime_common.sys.platform', return_value='linux')
    def test_go_fullscreen_linux(self, mock_platform, mock_pygame):
        mock_display = Mock()
        mock_display.convert = Mock()
        mock_display.get_caption = Mock(return_value=("Test", "Test"))
        mock_display.get_surface = Mock(return_value=mock_display)
        mock_pygame.display.get_surface = Mock(return_value=mock_display)
        mock_pygame.FULLSCREEN = 1
        mock_pygame.display.set_mode = Mock()

        screen = go_fullscreen()

        mock_pygame.display.init.assert_called_once()
        mock_pygame.display.set_mode.assert_called_with((0, 0), mock_pygame.FULLSCREEN, 0)
        self.assertEqual(screen, mock_display)

    @patch('src.ctime.ctime_common.pygame')
    @patch('src.ctime.ctime_common.sys.platform', return_value='darwin')
    def test_go_fullscreen_macos(self, mock_platform, mock_pygame):
        mock_display = Mock()
        mock_display.convert = Mock()
        mock_display.get_caption = Mock(return_value=("Test", "Test"))
        mock_display.get_surface = Mock(return_value=mock_display)
        mock_pygame.display.get_surface = Mock(return_value=mock_display)

        objc_mock = Mock()
        objc_mock.loadBundle = Mock()
        av_capture_device_mock = Mock()
        devices_mock = Mock()
        devices_mock.return_value = [av_capture_device_mock]

        with patch('src.ctime.ctime_common.objc', objc_mock):
            with patch('src.ctime.ctime_common.AVCaptureDevice', av_capture_device_mock):
                with patch('src.ctime.ctime_common.AVCaptureDevice.devices', devices_mock):
                    screen = go_fullscreen()

        mock_pygame.display.init.assert_called_once()
        self.assertEqual(screen, mock_display)

    @patch('src.ctime.ctime_common.pygame')
    @patch('src.ctime.ctime_common.sys.platform', return_value='other')
    def test_go_fullscreen_other_platform(self, mock_platform, mock_pygame):
        mock_display = Mock()
        mock_display.convert = Mock()
        mock_display.get_caption = Mock(return_value=("Test", "Test"))
        mock_display.get_surface = Mock(return_value=mock_display)
        mock_pygame.display.get_surface = Mock(return_value=mock_display)
        mock_pygame.display.set_mode = Mock()

        screen = go_fullscreen()

        mock_pygame.display.init.assert_called_once()
        mock_pygame.display.set_mode.assert_called_with((0, 0), 0, 0)
        self.assertEqual(screen, mock_display)

    @patch('src.ctime.ctime_common.os.path.exists', return_value=True)
    @patch('src.ctime.ctime_common.sys.platform', return_value='linux')
    def test_is_video_camera_present_linux(self, mock_platform, mock_exists):
        result = is_video_camera_present()
        self.assertTrue(result)

    @patch('src.ctime.ctime_common.os.path.exists', return_value=False)
    @patch('src.ctime.ctime_common.sys.platform', return_value='linux')
    def test_is_video_camera_present_linux_not_present(self, mock_platform, mock_exists):
        result = is_video_camera_present()
        self.assertFalse(result)

    @patch('src.ctime.ctime_common.objc')
    @patch('src.ctime.ctime_common.AVCaptureDevice')
    @patch('src.ctime.ctime_common.sys.platform', return_value='darwin')
    def test_is_video_camera_present_macos(self, mock_platform, mock_avcapture_device, mock_objc):
        mock_device = Mock()
        mock_device.hasMediaType_.return_value = True
        mock_avcapture_device.devices.return_value = [mock_device]

        result = is_video_camera_present()
        self.assertTrue(result)

    @patch('src.ctime.ctime_common.objc')
    @patch('src.ctime.ctime_common.AVCaptureDevice')
    @patch('src.ctime.ctime_common.sys.platform', return_value='darwin')
    def test_is_video_camera_present_macos_not_present(self, mock_platform, mock_avcapture_device, mock_objc):
        mock_device = Mock()
        mock_device.hasMediaType_.return_value = False
        mock_avcapture_device.devices.return_value = [mock_device]

        result = is_video_camera_present()
        self.assertFalse(result)

    @patch('src.ctime.ctime_common.os.path.exists', return_value=False)
    @patch('src.ctime.ctime_common.sys.platform', return_value='other')
    def test_is_video_camera_present_other_platform_not_present(self, mock_platform, mock_exists):
        result = is_video_camera_present()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

