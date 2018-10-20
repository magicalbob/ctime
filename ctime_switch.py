""" version of button that turns on/off power to light """
import time
import os
from ctime_button import Button

class Switch(Button):
    """ a switch for power """
    def __init__(self, screen, rect, image, colorkey, power_on, power_off):
        """ initialise the switch """
        Button.__init__(self, screen, rect, image, colorkey)
        self.power_state = False
        self.power_on = power_on
        self.power_off = power_off
        self.rpi_power()
        self.enabled = True
        self.button_time = time.time()
        self.light_time = time.time()

    def check_off(self):
        """ check if the switch should auto turn off """
        if self.power_state:
            if (time.time() - self.light_time) > 3600:
                self.power_state = False
                self.rpi_power()

    def check_button(self):
        """ check if the switch should reappear """
        if not self.enabled:
            if (time.time() - self.button_time) > 15:
                self.enabled = True
                return True
        return False

    def check_click(self, pos):
        """ check if the switch has been switched """
        if not self.enabled:
            return False

        return_val = Button.check_click(self, pos)

        if return_val:
            self.power_state = not self.power_state
            self.rpi_power()
            self.button_time = time.time()
            self.light_time = time.time()
            self.enabled = False

        return return_val

    def rpi_power(self):
        """ turn in or off the power """
        if self.power_state:
            os.spawnl(os.P_NOWAIT,self.power_on)
        else:
            os.spawnl(os.P_NOWAIT,self.power_off)
