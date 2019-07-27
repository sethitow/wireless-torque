import analogio
import binascii
import bleio
import board
import busio
import digitalio
import time
import microcontroller

import adafruit_adxl34x
from adafruit_ble.advertising import ServerAdvertisement

import ads1232

print("Running!")

voltage_monitor = analogio.AnalogIn(board.VOLTAGE_MONITOR)

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
battery_service = bleio.Service(bleio.UUID(0x180F), [battery_level_chara])

adc1_chara = bleio.Characteristic(bleio.UUID(0x2A58), read=True, notify=True)
adc2_chara = bleio.Characteristic(bleio.UUID(0x2A58), read=True, notify=True)
adc_service = bleio.Service(bleio.UUID(0x1815), [adc1_chara, adc2_chara])

device_uid = binascii.hexlify(microcontroller.cpu.uid)
periph_name = "".join(["TORQUE-", device_uid[-6:].decode("ascii")])
print("Starting peripherial with name: %s" % periph_name)
periph = bleio.Peripheral([battery_service, adc_service], name=periph_name)
periph.start_advertising()

while True:
    battery_voltage = (voltage_monitor.value * 3.3) / 65536 * 2
    battery_soc = int(250 * (battery_voltage - 3) / 3)

    mux_select.value = False
    ch1_value = adc.raw_read()

    mux_select.value = True
    ch2_value = adc.raw_read()

    if periph.connected:
        battery_level_chara.value = battery_soc.to_bytes(1, "big")
        adc1_chara.value = ch1_value.to_bytes(4, "big")
        adc2_chara.value = ch2_value.to_bytes(4, "big")

    print(
        "Accel: %f %f %f. ADC: %d %d. Battery: %fv %d%"
        % (
            accelerometer.acceleration[0],
            accelerometer.acceleration[1],
            accelerometer.acceleration[2],
            ch1_value,
            ch2_value,
            battery_voltage,
            battery_soc,
        )
    )
    time.sleep(0.2)
