from digitalio import DigitalInOut, Direction, Pull

class Button:
    def __init__(self, pin):
        self.gpio = DigitalInOut(pin)
        self.gpio.direction = Direction.INPUT
        self.gpio.pull = Pull.UP

        self.state = False

    def is_pressed(self):
        old_state = self.state
        # The button reads 0 when pressed, so invert it
        self.state = not self.gpio.value
        if not old_state and self.state:
            return True
        return False
