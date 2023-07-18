import unittest
from unittest.mock import MagicMock
from src.ctime.ctime_switch import Switch

class CtimeSwitchTestCase(unittest.TestCase):
    def setUp(self):
        self.screen = MagicMock()
        self.rect = (0, 0, 100, 100)
        self.image = "switch.png"
        self.colorkey = (255, 255, 255)
        self.power_on = "power_on.sh"
        self.power_off = "power_off.sh"
        self.log = MagicMock()
        self.switch = Switch(self.screen, self.rect, self.image, self.colorkey, self.power_on, self.power_off, self.log)

    def test_initialization(self):
        self.assertEqual(self.switch.log, self.log)
        self.log.info.assert_called_with('initialise power switch')
        self.assertTrue(isinstance(self.switch, Switch))
        self.assertTrue(isinstance(self.switch, Button))
        self.assertEqual(self.switch.power_state, False)
        self.assertEqual(self.switch.power_on, self.power_on)
        self.assertEqual(self.switch.power_off, self.power_off)
        self.switch.rpi_power.assert_called()
        self.assertEqual(self.switch.enabled, True)
        self.assertIsInstance(self.switch.button_time, float)
        self.assertIsInstance(self.switch.light_time, float)

    def test_check_off(self):
        self.switch.power_state = True
        self.switch.light_time = 0
        self.switch.rpi_power = MagicMock()
        self.switch.check_off()
        self.assertFalse(self.switch.power_state)
        self.switch.rpi_power.assert_called()

        self.switch.power_state = True
        self.switch.light_time = time.time()
        self.switch.rpi_power = MagicMock()
        self.switch.check_off()
        self.assertFalse(self.switch.power_state)
        self.switch.rpi_power.assert_called()

        self.switch.power_state = False
        self.switch.light_time = 0
        self.switch.rpi_power = MagicMock()
        self.switch.check_off()
        self.assertFalse(self.switch.rpi_power.called)

        self.switch.power_state = False
        self.switch.light_time = time.time()
        self.switch.rpi_power = MagicMock()
        self.switch.check_off()
        self.assertFalse(self.switch.rpi_power.called)

    def test_check_button(self):
        self.switch.enabled = False
        self.switch.button_time = 0
        self.assertFalse(self.switch.check_button())

        self.switch.enabled = False
        self.switch.button_time = time.time()
        self.assertFalse(self.switch.check_button())

        self.switch.enabled = True
        self.switch.button_time = 0
        self.assertFalse(self.switch.check_button())

        self.switch.enabled = True
        self.switch.button_time = time.time()
        self.assertFalse(self.switch.check_button())

        self.switch.enabled = False
        self.switch.button_time = time.time() - 16
        self.assertTrue(self.switch.check_button())
        self.assertTrue(self.switch.enabled)

    def test_check_click(self):
        pos = (50, 50)

        # Test when switch is not enabled
        self.switch.enabled = False
        self.switch.button_time = time.time()
        self.assertFalse(self.switch.check_click(pos))
        self.assertFalse(self.switch.power_state)
        self.assertFalse(self.switch.rpi_power.called)
        self.assertEqual(self.switch.button_time, time.time())
        self.assertEqual(self.switch.light_time, time.time())
        self.assertFalse(self.switch.enabled)

        # Test when switch is enabled
        self.switch.enabled = True
        self.switch.check_click(pos)
        self.assertTrue(self.switch.power_state)
        self.switch.rpi_power.assert_called()
        self.assertEqual(self.switch.button_time, time.time())
        self.assertEqual(self.switch.light_time, time.time())
        self.assertFalse(self.switch.enabled)

        # Test when switch is clicked again
        self.switch.power_state = True
        self.switch.rpi_power.reset_mock()
        self.switch.check_click(pos)
        self.assertFalse(self.switch.power_state)
        self.switch.rpi_power.assert_called()
        self.assertEqual(self.switch.button_time, time.time())
        self.assertEqual(self.switch.light_time, time.time())
        self.assertFalse(self.switch.enabled)

    def test_rpi_power(self):
        self.switch.power_state = True
        self.switch.rpi_power()
        self.log.info.assert_called_with('turn on or off the power')
        self.log.info.assert_called_with('turn power on')
        os.system.assert_called_with(self.power_on)

        self.switch.power_state = False
        self.switch.rpi_power()
        self.log.info.assert_called_with('turn on or off the power')
        self.log.info.assert_called_with('turn power off')
        os.system.assert_called_with(self.power_off)

if __name__ == '__main__':
    unittest.main()

