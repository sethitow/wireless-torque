import time
import board
import busio
import adafruit_adxl34x
import ads1232
import digitalio

print("Running!")

pin_data_out = board.MISO
pin_clock = board.SCK
pin_power_down = board.D10
pin_speed = board.D9
pin_temp = board.D11
pin_mux_select = board.D12
pin_gain1 = board.D5
pin_gain2 = board.D6

speed = digitalio.DigitalInOut(pin_speed)
speed.direction = digitalio.Direction.OUTPUT
speed.drive_mode = digitalio.DriveMode.PUSH_PULL

temp = digitalio.DigitalInOut(pin_temp)
temp.direction = digitalio.Direction.OUTPUT
temp.drive_mode = digitalio.DriveMode.PUSH_PULL

mux_select = digitalio.DigitalInOut(pin_mux_select)
mux_select.direction = digitalio.Direction.OUTPUT
mux_select.drive_mode = digitalio.DriveMode.PUSH_PULL

gain1 = digitalio.DigitalInOut(pin_gain1)
gain1.direction = digitalio.Direction.OUTPUT
gain1.drive_mode = digitalio.DriveMode.PUSH_PULL

gain2 = digitalio.DigitalInOut(pin_gain2)
gain2.direction = digitalio.Direction.OUTPUT
gain2.drive_mode = digitalio.DriveMode.PUSH_PULL

speed.value = False
temp.value = False
mux_select.value = False
gain1.value = True
gain2.value = True


adc = ads1232.ADS1232(pin_power_down, pin_clock, pin_data_out)
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
adc.reset()

while True:

    mux_select.value = False
    ch1_value = adc.raw_read()
    mux_select.value = True
    ch2_value = adc.raw_read()
    print("%f %f %f %d %d"% (accelerometer.acceleration[0], accelerometer.acceleration[1], accelerometer.acceleration[2], ch1_value, ch2_value))
    time.sleep(0.2)
