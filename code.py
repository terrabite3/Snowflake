import board
import time

import supervisor

from display import *
from button import *
from accelerometer import *
from mode import *

display = Display(0, 60)

button_left = Button(board.MODE_L)
button_right = Button(board.MODE_R)

accel = Accelerometer()


mode_switcher = ModeSwitcher(display, accel)


while True:
    start_time = time.monotonic()

    current_mode = mode_switcher.get_current_mode()

    current_mode.draw()

    # Busy-wait until the mode's delay period has elapsed
    while time.monotonic() - start_time < current_mode.delay:
        pass

    if button_left.is_pressed():
        mode_switcher.advance_mode_group()
    if button_right.is_pressed():
        mode_switcher.advance_mode()
