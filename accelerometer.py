import adafruit_lis3dh
import board
from digitalio import DigitalInOut

class Accelerometer:
    def __init__(self):
        self.i2c = board.I2C()
        self.int1 = DigitalInOut(board.INT1)
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c, int1=self.int1, address=0x19)
