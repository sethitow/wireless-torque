import bleio
import board
import busio
import digitalio
import time

import adafruit_adxl34x
from adafruit_ble.advertising import ServerAdvertisement

import ads1232

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


battery_level_chara = bleio.Characteristic(bleio.UUID(0x2919), read=True, notify=True)
battery_service = bleio.Service(bleio.UUID(0x180f), [battery_level_chara])

adc1_chara = bleio.Characteristic(bleio.UUID(0x2A58), read=True, notify=True)
adc2_chara = bleio.Characteristic(bleio.UUID(0x2A58), read=True, notify=True)
adc_service = bleio.Service(bleio.UUID(0x1815), [adc1_chara, adc2_chara])

# Create a peripheral and start it up.
periph = bleio.Peripheral([battery_service, adc_service])
periph.start_advertising()

while True:

    mux_select.value = False
    ch1_value = adc.raw_read()
    # adc1_chara.value = ch1_value.to_bytes(3, 'big')
    adc1_chara.value = bytes(0x00)

    mux_select.value = True
    ch2_value = adc.raw_read()
    # adc2_chara.value = ch2_value.to_bytes(3, 'big')

    print("%f %f %f %d %d"% (accelerometer.acceleration[0], accelerometer.acceleration[1], accelerometer.acceleration[2], ch1_value, ch2_value))
    time.sleep(0.2)
