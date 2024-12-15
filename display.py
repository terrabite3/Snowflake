import xmas3

class Led:
    def __init__(self, index):
        self.index = index

    def set(self, value):
        if value < 0:
            value = 0
        if value > 255:
            value = 255
        xmas3.set_led(self.index, value)

    def get(self):
        return xmas3.get_led(self.index)

    def add(self, value):
        self.set(self.get() + value)

    def subtract(self, value):
        self.set(self.get() - value)

class Display:
    def __init__(self, polling_delay_us = None, min_freq = None):
        # The display loop runs in the second core of the RP2040.
        # It uses a LUT (lookup table) to apply gamma correction to the LEDs,
        # so that they appear to dim evenly over the full range of values.
        # If the LEDs flash too slowly, the flashing becomes visible.
        # So here we can specify the minimum frequency (default 30 Hz).
        # We can also specify the delay in the loop, which determines the
        # minimum LUT value which will produce flashing of the minimum frequency.
        #
        # TL;DR:
        # * Increasing min_freq will make the LEDs less flickery at the lowest values,
        #   but it will increase the brightness of the lowest values.
        # * Decreasing polling_delay_us decrease the brightness of the lowest values,
        #   but below 50 I've noticed odd behavior with the USB connection.
        if polling_delay_us == None:
            xmas3.start_display()
        elif min_freq == None:
            xmas3.start_display(polling_delay_us)
        else:
            xmas3.start_display(polling_delay_us, min_freq)

        self.A0 = Led(7)
        self.A1 = Led(6)
        self.A2 = Led(5)
        self.A3 = Led(2)
        self.A4 = Led(3)
        self.A5 = Led(4)
        self.A6 = Led(1)
        self.A7 = Led(0)
        self.B0 = Led(47)
        self.B1 = Led(46)
        self.B2 = Led(45)
        self.B3 = Led(42)
        self.B4 = Led(43)
        self.B5 = Led(44)
        self.B6 = Led(41)
        self.B7 = Led(40)
        self.C0 = Led(39)
        self.C1 = Led(38)
        self.C2 = Led(37)
        self.C3 = Led(34)
        self.C4 = Led(35)
        self.C5 = Led(36)
        self.C6 = Led(33)
        self.C7 = Led(32)
        self.D0 = Led(31)
        self.D1 = Led(30)
        self.D2 = Led(29)
        self.D3 = Led(26)
        self.D4 = Led(27)
        self.D5 = Led(28)
        self.D6 = Led(25)
        self.D7 = Led(24)
        self.E0 = Led(23)
        self.E1 = Led(22)
        self.E2 = Led(21)
        self.E3 = Led(18)
        self.E4 = Led(19)
        self.E5 = Led(20)
        self.E6 = Led(17)
        self.E7 = Led(16)
        self.F0 = Led(15)
        self.F1 = Led(14)
        self.F2 = Led(13)
        self.F3 = Led(10)
        self.F4 = Led(11)
        self.F5 = Led(12)
        self.F6 = Led(9)
        self.F7 = Led(8)

        self.ARM_A = [self.A0, self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7]
        self.ARM_B = [self.B0, self.B1, self.B2, self.B3, self.B4, self.B5, self.B6, self.B7]
        self.ARM_C = [self.C0, self.C1, self.C2, self.C3, self.C4, self.C5, self.C6, self.C7]
        self.ARM_D = [self.D0, self.D1, self.D2, self.D3, self.D4, self.D5, self.D6, self.D7]
        self.ARM_E = [self.E0, self.E1, self.E2, self.E3, self.E4, self.E5, self.E6, self.E7]
        self.ARM_F = [self.F0, self.F1, self.F2, self.F3, self.F4, self.F5, self.F6, self.F7]

        self.ARMS = [self.ARM_A, self.ARM_B, self.ARM_C, self.ARM_D, self.ARM_E, self.ARM_F]

        # The inner ring of 6 LEDs, starting with the one on top, going clockwise
        self.RING_A = [self.A0, self.B0, self.C0, self.D0, self.E0, self.F0]
        # The second ring, starting at top, going clockwise
        self.RING_B1 = [self.A3, self.A2, self.B1, self.B3, self.B2, self.C1, self.C3, self.C2, self.D1, self.D3, self.D2, self.E1, self.E3, self.E2, self.F1, self.F3, self.F2, self.A1]
        # The third ring, which shares some with the second ring
        self.RING_B2 = [self.A3, self.A5, self.B4, self.B3, self.B5, self.C4, self.C3, self.C5, self.D4, self.D3, self.D5, self.E4, self.E3, self.E5, self.F4, self.F3, self.F5, self.A4]
        self.RING_C = [self.A6, self.B6, self.C6, self.D6, self.E6, self.F6]
        self.RING_D = [self.A7, self.B7, self.C7, self.D7, self.E7, self.F7]

        self.ALL = [
            self.A0,
            self.A1,
            self.A2,
            self.A3,
            self.A4,
            self.A5,
            self.A6,
            self.A7,
            self.B0,
            self.B1,
            self.B2,
            self.B3,
            self.B4,
            self.B5,
            self.B6,
            self.B7,
            self.C0,
            self.C1,
            self.C2,
            self.C3,
            self.C4,
            self.C5,
            self.C6,
            self.C7,
            self.D0,
            self.D1,
            self.D2,
            self.D3,
            self.D4,
            self.D5,
            self.D6,
            self.D7,
            self.E0,
            self.E1,
            self.E2,
            self.E3,
            self.E4,
            self.E5,
            self.E6,
            self.E7,
            self.F0,
            self.F1,
            self.F2,
            self.F3,
            self.F4,
            self.F5,
            self.F6,
            self.F7,
        ]

    def set_all(self, value):
        for i in range(48):
            xmas3.set_led(i, value)

    def add_all(self, value):
        for i in range(48):
            val = xmas3.get_led(i)
            val += value
            if val > 255:
                val = 255
            xmas3.set_led(i, val)

    def subtract_all(self, value):
        for i in range(48):
            val = xmas3.get_led(i)
            val -= value
            if val < 0:
                val = 0
            xmas3.set_led(i, val)
