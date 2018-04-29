""" version of button that turns on/off power to light """
import time
import os
from ctime_button import Button

class Switch(Button):
    """ a switch for power """
    def __init__(self, screen, rect, image, colorkey):
        """ initialise the switch """
        Button.__init__(self, screen, rect, image, colorkey)
        self.power_state = False
        rpi_power(self.power_state)
        self.enabled = True
        self.button_time = time.time()
        self.light_time = time.time()

    def check_off(self):
        """ check if the switch should auto turn off """
        if self.power_state:
            if (time.time() - self.light_time) > 3600:
                self.power_state = False
                rpi_power(self.power_state)

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
            rpi_power(self.power_state)
            self.button_time = time.time()
            self.light_time = time.time()
            self.enabled = False

        return return_val

def rpi_power(state):
    """ turn in or off the power """
    if os.uname()[1].startswith('rpi21'):
        if state:
            os.system("sudo ./rpion.py")
        else:
            os.system("sudo ./rpioff.py")
    else:
        print "NOT A PI. New state: "+str(state)
