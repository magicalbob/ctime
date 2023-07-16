""" version of button that turns on/off power to light """
import time
import os
from src.ctime.ctime_button import Button

class Switch(Button):
    """ a switch for power """
    def __init__(self, screen, rect, image, colorkey, power_on, power_off, log):
        """ initialise the switch """
        self.log = log
        self.log.info('initialise power switch')
        Button.__init__(self, screen, rect, image, colorkey, "Switch", self.log)
        self.power_state = False
        self.power_on = power_on
        self.power_off = power_off
        self.rpi_power()
        self.enabled = True
        self.button_time = time.time()
        self.light_time = time.time()

    def check_off(self):
        """ check if the switch should auto turn off """
        if self.power_state and (time.time() - self.light_time) > 3600:
            self.power_state = False
            self.rpi_power()

    def check_button(self):
        """ check if the switch should reappear """
        if not self.enabled and (time.time() - self.button_time) > 15:
                self.enabled = True
                return True
        return False

    def check_click(self, pos):
        """ check if the switch has been switched """
        if not self.enabled:
            return False

        return_val = Button.check_click(self, pos)

        if return_val:
            self.log.info('power switch clicked')
            self.power_state = not self.power_state
            self.log.info('call rpi_power')
            self.rpi_power()
            self.log.info('set button off time')
            self.button_time = time.time()
            self.log.info('set light on time')
            self.light_time = time.time()
            self.log.info('disable switch')
            self.enabled = False

        return return_val

    def rpi_power(self):
        """ turn on or off the power """
        self.log.info('turn on or off the power')
        if self.power_state:
            self.log.info('turn power on')
            os.system(self.power_on)
        else:
            self.log.info('turn power off')
            os.system(self.power_off)
