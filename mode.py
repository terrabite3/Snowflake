
import time
import gc
import math
import random
import microcontroller

class BlinkMode:
    def __init__(self, display):
        self.__display = display
        self.delay = 0.01
        self.counter = 0

    def start(self):
        pass

    def draw(self):
        self.counter += 1
        if self.counter >= 200:
            self.counter = 0
        if self.counter < 100:
            self.__display.set_all(255)
        else:
            self.__display.set_all(0)


class ConstantMode:
    def __init__(self, display, value):
        self.display = display
        self.delay = 0.01
        self.value = value

    def start(self):
        pass

    def draw(self):
        self.display.set_all(self.value)

class FadeInMode:
    def __init__(self, display, delay):
        self.display = display
        self.delay = delay
        self.counter = 0

    def start(self):
        pass

    def draw(self):
        self.counter = (self.counter + 1) % 256
        self.display.set_all(self.counter)

# This mode demonstrates using get_led().
# It could be implemented easily without it, but the point is to demo it.
class PulseMode:
    def __init__(self, display, delay):
        self.display = display
        self.delay = delay
        self.counter = 0

    def start(self):
        self.counter = 0

    def draw(self):
        if self.counter == 0:
            self.display.set_all(255)
        else:
            self.display.subtract_all(1)

        self.counter = (self.counter + 1) % 500

class StarburstMode:
    def __init__(self, display, delay):
        self.display = display
        self.delay = delay
        self.counter = 0
        self.profile = True

    def start(self):
        self.counter = 0

    def draw(self):
        if self.profile:
            gc.collect()
            gc.disable()

            start_time = time.monotonic()
            self.display.subtract_all(1)
            duration = time.monotonic() - start_time
            print(duration)
            self.profile = False

            gc.enable()
        else:
            self.display.subtract_all(1)
        
        ring_index = self.counter // 30
        if ring_index == 0:
            ring = self.display.RING_A
        elif ring_index == 1:
            ring = self.display.RING_B1
        elif ring_index == 2:
            ring = self.display.RING_B2
        elif ring_index == 3:
            ring = self.display.RING_C
        elif ring_index == 4:
            ring = self.display.RING_D
        else:
            ring = []
        
        for led in ring:
            led.add(10)

        self.counter = (self.counter + 1) % 300

class AccelPlumb:
    def __init__(self, display, accel):
        self.display = display
        self.accel = accel
        self.delay = 0.004

    def start(self):
        self.display.set_all(0)

    def draw(self):
        self.display.subtract_all(4)

        acc_vector = self.accel.lis3dh.acceleration
        print(acc_vector)

        # If you hold it still in some orientation, gravity will read as follows.
        # +Y is down (bottom arm of snowflake), -Y is up
        # +X is left, -X is right
        # +Z is in (toward the snowflake as you look at the front), -Z is out

        # We'll take the dot product with six normalized vectors pointing in the
        # directions of the arms. Whichever is greatest is the arm that's pointing down.
        arm_vectors = [
            ( 0.0,   -1.0, 0),
            (-0.866, -0.5, 0),
            (-0.866,  0.5, 0),
            ( 0.0,    1.0, 0),
            ( 0.866,  0.5, 0),
            ( 0.866, -0.5, 0),
        ]

        max_dot_product = 0
        max_index = -1

        for i in range(len(arm_vectors)):
            vector_i = arm_vectors[i]
            dot = acc_vector[0] * vector_i[0] + acc_vector[1] * vector_i[1] + acc_vector[2] * vector_i[2]
            if dot > max_dot_product:
                max_dot_product = dot
                max_index = i

        if max_index == -1:
            print("Error: no max dot product")

        # Light the arm pointing down, brighter at the tip
        self.display.ARMS[max_index][7].set(255)
        self.display.ARMS[max_index][6].set(220)
        self.display.ARMS[max_index][5].set(180)
        self.display.ARMS[max_index][4].set(180)
        self.display.ARMS[max_index][3].set(160)
        self.display.ARMS[max_index][2].set(120)
        self.display.ARMS[max_index][1].set(120)
        self.display.ARMS[max_index][0].set(100)

class AccelActivity:
    def __init__(self, display, accel):
        self.__display = display
        self.__accel = accel
        self.__last_vector = self.__accel.lis3dh.acceleration
        self.delay = 0.010

        self.__accumulator = 0

    def start(self):
        self.__display.set_all(0)

    def draw(self):
        acc_vector = self.__accel.lis3dh.acceleration
        jerk = math.sqrt((acc_vector[0] - self.__last_vector[0]) ** 2 + (acc_vector[1] - self.__last_vector[1]) ** 2 + (acc_vector[2] - self.__last_vector[2]) ** 2)
        self.__last_vector = acc_vector

        self.__accumulator += jerk
        # print(jerk)

        self.__display.subtract_all(1)
        for foo in [16, 8, 4, 2, 1]:
            if self.__accumulator > foo:
                self.__accumulator -= foo
                i = random.randint(0, 47)
                self.__display.ALL[i].add(foo * 16)

class AccelMarble:
    def __init__(self, display, accel):
        self.display = display
        self.accel = accel
        self.delay = 0.004

        self.marble_pos = (0, 0)

        self.led_positions = [
            (0, -10), # A0
            ()
        ]

    def start(self):
        self.display.set_all(0)

    def draw(self):
        self.display.subtract_all(4)

        acc_vector = self.accel.lis3dh.acceleration
        print(acc_vector)

        # If you hold it still in some orientation, gravity will read as follows.
        # +Y is down (bottom arm of snowflake), -Y is up
        # +X is left, -X is right
        # +Z is in (toward the snowflake as you look at the front), -Z is out

        force_vector = (acc_vector[0], acc_vector[1])

        # We'll take the dot product with six normalized vectors pointing in the
        # directions of the arms. Whichever is greatest is the arm that's pointing down.
        arm_vectors = [
            ( 0.0,   -1.0, 0),
            (-0.866, -0.5, 0),
            (-0.866,  0.5, 0),
            ( 0.0,    1.0, 0),
            ( 0.866,  0.5, 0),
            ( 0.866, -0.5, 0),
        ]

        max_dot_product = 0
        max_index = -1

        for i in range(len(arm_vectors)):
            vector_i = arm_vectors[i]
            dot = acc_vector[0] * vector_i[0] + acc_vector[1] * vector_i[1] + acc_vector[2] * vector_i[2]
            if dot > max_dot_product:
                max_dot_product = dot
                max_index = i

        if max_index == -1:
            print("Error: no max dot product")

        # Light the arm pointing down, brighter at the tip
        self.display.ARMS[max_index][7].set(255)
        self.display.ARMS[max_index][6].set(220)
        self.display.ARMS[max_index][5].set(180)
        self.display.ARMS[max_index][4].set(180)
        self.display.ARMS[max_index][3].set(160)
        self.display.ARMS[max_index][2].set(120)
        self.display.ARMS[max_index][1].set(120)
        self.display.ARMS[max_index][0].set(100)

class MitxelaMode:
    def __init__(self, display):
        self.__display = display
        self.delay = 0.001
        self.__counter = 0

    def start(self):
        self.__display.set_all(0)

    def draw(self):
        self.__counter += 1
        for i in range(48):
            led = self.__display.ALL[i]

            val = int((self.__counter * 1000) / (1000 + i)) % 600
            if val < 256:
                led.set(val)
            elif val < 512:
                led.set(512 - val)
            else:
                led.set(0)


class SwirlMode:
    def __init__(self, display):
        self.__display = display
        self.delay = 0.005
        self.__counter = 0

        self.__order = [
            self.__display.A0,
            self.__display.B0,
            self.__display.C0,
            self.__display.D0,
            self.__display.E0,
            self.__display.F0,

            self.__display.A2,
            self.__display.B1,
            self.__display.B3,
            self.__display.B2,
            self.__display.C1,
            self.__display.C3,
            self.__display.C2,
            self.__display.D1,
            self.__display.D3,
            self.__display.D2,
            self.__display.E1,
            self.__display.E3,
            self.__display.E2,
            self.__display.F1,
            self.__display.F3,
            self.__display.F2,
            self.__display.A1,
            self.__display.A3,

            self.__display.A5,
            self.__display.B4,
            self.__display.B5,
            self.__display.C4,
            self.__display.C5,
            self.__display.D4,
            self.__display.D5,
            self.__display.E4,
            self.__display.E5,
            self.__display.F4,
            self.__display.F5,
            self.__display.A4,

            self.__display.A6,
            self.__display.B6,
            self.__display.C6,
            self.__display.D6,
            self.__display.E6,
            self.__display.F6,

            self.__display.A7,
            self.__display.B7,
            self.__display.C7,
            self.__display.D7,
            self.__display.E7,
            self.__display.F7,
        ]

    def start(self):
        self.__display.set_all(0)

    def draw(self):
        self.__display.subtract_all(1)

        self.__counter += 1
        index = (self.__counter // 20) % len(self.__order)
        self.__order[index].set(255)
        

class LoopMode:
    def __init__(self, display, arms=1):
        self.__display = display
        self.delay = 0.005

        self.__counter = 0
        self.__arms = arms

    def start(self):
        self.__counter = 0
        self.__display.set_all(0)

    def draw(self):
        self.__display.subtract_all(2)

        self.__counter += 1
        foo = self.__counter // 20
        step = foo % 9
        arm_index = (foo // 9) % 6
        if step == 0:
            index = 0
        elif step == 1:
            index = 1
        elif step == 2:
            index = 4
        elif step == 3:
            index = 6
        elif step == 4:
            index = 7
        elif step == 5:
            index = 6
        elif step == 6:
            index = 5
        elif step == 7:
            index = 2
        elif step == 8:
            index = 0

        if self.__arms == 1:
            self.__display.ARMS[-arm_index][index].set(255)
        elif self.__arms == 2:
            self.__display.ARMS[-arm_index][index].set(255)
            self.__display.ARMS[-arm_index + 3][index].set(255)
        elif self.__arms == 3:
            self.__display.ARMS[-arm_index][index].set(255)
            self.__display.ARMS[-arm_index + 2][index].set(255)
            self.__display.ARMS[-arm_index + 4][index].set(255)



# Radiate out and in


class ShowModeMode:
    def __init__(self, display):
        self.display = display
        self.mode_group = 0
        self.mode_index = 0
        self.delay = 0.01
        self.show_index = False

    def start(self):
        pass

    def draw(self):
        self.display.set_all(0)
        self.display.RING_A[self.mode_group].set(255)

        if self.show_index:
            self.display.RING_B1[self.mode_index].set(255)


class ModeSwitcher:
    def __init__(self, display, accel):
        self.modes = [
            [
                ConstantMode(display, 255),
                ConstantMode(display, 128),
                ConstantMode(display, 64),
                ConstantMode(display, 32),
                ConstantMode(display, 16),
                ConstantMode(display, 14),
                ConstantMode(display, 12),
                ConstantMode(display, 11),
                ConstantMode(display, 10),
                ConstantMode(display, 9),
                ConstantMode(display, 8),
                ConstantMode(display, 7),
                ConstantMode(display, 6),
                ConstantMode(display, 5),
                ConstantMode(display, 4),
                ConstantMode(display, 3),
                ConstantMode(display, 2),
                ConstantMode(display, 1),
            ],
            [
                FadeInMode(display, 0.01),
                FadeInMode(display, 0.001),
                PulseMode(display, 0.001),
                StarburstMode(display, 0.00001),
                MitxelaMode(display),
                SwirlMode(display),
                LoopMode(display, 1),
                LoopMode(display, 2),
                LoopMode(display, 3),
            ],
            [
                AccelPlumb(display, accel),
                AccelActivity(display, accel),
                AccelMarble(display, accel),
            ],
            [
                BlinkMode(display),
            ],
        ]

        self.mode_group = 0
        self.mode_index = 0
        self.load_mode()

        self.countdown = 200

        self.first_boot = True

        self.show_mode_mode = ShowModeMode(display)
        self.show_mode_mode.mode_group = self.mode_group
        self.show_mode_mode.mode_index = self.mode_index


    def get_current_mode(self):
        if self.countdown > 0:
            self.countdown -= 1
            self.show_mode_mode.show_index = (self.countdown < 150)
            return self.show_mode_mode
        else:
            mode = self.modes[self.mode_group][self.mode_index]
            if self.countdown == 0:
                self.countdown -= 1
                mode.start()

                # Don't save the mode if we just turned on, only if the user actually changed the mode
                if self.first_boot:
                    self.first_boot = False
                else:
                    self.save_mode()
            return mode

    def advance_mode_group(self):
        self.mode_group = (self.mode_group + 1) % len(self.modes)
        self.mode_index = 0
        if self.countdown > 0:
            self.countdown = 100
        else:
            self.countdown = 200
        self.show_mode_mode.mode_group = self.mode_group
        self.show_mode_mode.mode_index = self.mode_index

    def advance_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes[self.mode_group])
        if self.countdown > 0:
            self.countdown = 100
        else:
            self.countdown = 200
        self.show_mode_mode.mode_group = self.mode_group
        self.show_mode_mode.mode_index = self.mode_index


    def load_mode(self):
        if len(microcontroller.nvm) < 2:
            print('No mode stored in nvm')
            return

        mode_group = microcontroller.nvm[0]
        mode_index = microcontroller.nvm[1]
        if mode_group >= len(self.modes):
            print('Loaded mode group out of range')
            return
        if mode_index >= len(self.modes[mode_group]):
            print('Loaded mode index out of range')
            return

        print('Loading mode {}, {}'.format(mode_group, mode_index))
        self.mode_group = mode_group
        self.mode_index = mode_index

    def save_mode(self):
        print('Saving mode {}, {}'.format(self.mode_group, self.mode_index))
        microcontroller.nvm[0:2] = bytes([self.mode_group, self.mode_index])

