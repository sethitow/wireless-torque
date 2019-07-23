import bitbangio
import digitalio
import busio
import time


GAIN_1 = 0b00
GAIN_2 = 0b10
GAIN_64 = 0b01
GAIN_128 = 0b11


class ADS1232:
    def __init__(self, power_down, clock, data_out):

        self._power_down = digitalio.DigitalInOut(power_down)
        self._power_down.direction = digitalio.Direction.OUTPUT
        self._power_down.drive_mode = digitalio.DriveMode.PUSH_PULL

        self._clock = digitalio.DigitalInOut(clock)
        self._clock.direction = digitalio.Direction.OUTPUT
        self._clock.drive_mode = digitalio.DriveMode.PUSH_PULL

        self._data_out = digitalio.DigitalInOut(data_out)
        self._data_out.direction = digitalio.Direction.INPUT

    def reset(self):
        print("Resetting!")
        self._power_down.value = False
        self._power_down.value = True

    def raw_read(self):

        while self._data_out.value:
            pass

        while not self._data_out.value:
            pass

        result = bytearray(3)

        for i in range(0, 8):
            self._clock.value = True
            result[0] = result[0] | self._data_out.value << i
            self._clock.value = False

        for i in range(0, 8):
            self._clock.value = True
            result[1] = result[1] | self._data_out.value << i
            self._clock.value = False

        for i in range(0, 8):
            self._clock.value = True
            result[2] = result[2] | self._data_out.value << i
            self._clock.value = False

        return int.from_bytes(result, "big", True)

