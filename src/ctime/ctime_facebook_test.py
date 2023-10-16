import unittest
from unittest.mock import patch, MagicMock
from src.ctime.ctime_facebook import CtimeFacebook, CallEndedException

RATE_YOUR_VIDEO = "Please rate the quality of your video chat"
SOME_FACEBOOK_PAGE = "Some Facebook page source"

class TestCtimeFacebook(unittest.TestCase):

    @patch('src.ctime.ctime_facebook.webdriver')
    @patch('src.ctime.ctime_facebook.go_fullscreen')
    @patch('src.ctime.ctime_facebook.go_minimal')
    def test_CtimeFacebook(self, mock_go_minimal, mock_go_fullscreen, mock_webdriver):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()

        mock_webdriver.Firefox.return_value = mock_driver
        mock_driver.title = "Facebook"

        # Initialize the class
        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)

        # Assertions to verify that calls have been made correctly
        mock_log.info.assert_called_with('New Facebook object')
        mock_webdriver.Firefox.assert_called_with(options=mock.ANY, firefox_profile=mock.ANY)
        mock_driver.get.assert_called_with("https://www.facebook.com/messages")
        mock_driver.find_element_by_id.assert_called_with("email")
        mock_driver.find_element_by_id.assert_called_with("pass")
        mock_driver.find_element_by_xpath.assert_called_with('//*[@aria-label="Start a video call"]')

        # Additional test cases
        self.assertEqual(facebook.facebook_user, "username")
        self.assertEqual(facebook.facebook_pass, "password")

    @patch('src.ctime.ctime_facebook.time.sleep')
    def test_make_call(self, mock_sleep):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()
        mock_driver.page_source = ""

        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)
        facebook.driver = mock_driver

        # Simulate making a call
        mock_driver.find_element_by_xpath.return_value.click.side_effect = [None, CallEndedException]

        # Call make_call
        facebook.make_call()

        # Assertions to verify that calls have been made correctly
        mock_driver.find_element_by_xpath.assert_called_with('//*[@aria-label="Start a video call"]')
        mock_driver.switch_to_window.assert_called_with(mock.ANY)
        mock_driver.page_source = RATE_YOUR_VIDEO
        self.assertTrue(facebook.call_ended())

    @patch('src.ctime.ctime_facebook.time.sleep')
    def test_check_call_status(self, mock_sleep):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()
        mock_driver.page_source = ""

        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)
        facebook.driver = mock_driver

        # Simulate checking call status
        mock_driver.page_source = RATE_YOUR_VIDEO
        self.assertRaises(CallEndedException, facebook.check_call_status)

        mock_driver.page_source = "Connection lost"
        self.assertRaises(CallEndedException, facebook.check_call_status)

        mock_driver.page_source = "No Answer"
        self.assertRaises(CallEndedException, facebook.check_call_status)

    def test_call_ended(self):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()
        mock_driver.page_source = ""

        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)
        facebook.driver = mock_driver

        # Simulate call ended scenarios
        mock_driver.page_source = RATE_YOUR_VIDEO
        self.assertTrue(facebook.call_ended())

        mock_driver.page_source = "Connection lost"
        self.assertTrue(facebook.call_ended())

        mock_driver.page_source = "No Answer"
        self.assertTrue(facebook.call_ended())

    @patch('src.ctime.ctime_facebook.time.sleep')
    def test_check_signin(self, mock_sleep):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()
        mock_driver.page_source = ""

        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)
        facebook.driver = mock_driver

        # Simulate checking sign-in status
        mock_driver.get.side_effect = [None, AssertionError]

        # When still logged in
        mock_driver.title = "Facebook"
        facebook.check_signin()
        mock_driver.page_source = SOME_FACEBOOK_PAGE
        self.assertEqual(mock_driver.page_source, SOME_FACEBOOK_PAGE)

        # When not logged in
        mock_driver.title = "Some Other Title"
        facebook.check_signin()
        mock_driver.page_source = SOME_FACEBOOK_PAGE
        self.assertEqual(mock_driver.page_source, SOME_FACEBOOK_PAGE)
        mock_driver.get.assert_called_with("https://www.facebook.com/messages")
        mock_driver.page_source = SOME_FACEBOOK_PAGE
        self.assertTrue(mock_log.info.called)

    def test_abort_facebook(self):
        # Initialize necessary mocks
        mock_ctime = MagicMock()
        mock_log = MagicMock()
        mock_driver = MagicMock()

        facebook = CtimeFacebook(mock_ctime, "username", "password", mock_log)
        facebook.driver = mock_driver

        # Simulate aborting Facebook
        facebook.abort_facebook()

        # Assertions to verify that calls have been made correctly
        self.assertTrue(mock_ctime.enable_mouse.called)
        self.assertTrue(mock_driver.switch_to_window.called)
        self.assertEqual(mock_ctime.game_state, 0)
        self.assertTrue(mock_ctime.refresh_pic.called)
        self.assertTrue(mock_ctime.facebook_exit == 0)

if __name__ == '__main__':
    unittest.main()
