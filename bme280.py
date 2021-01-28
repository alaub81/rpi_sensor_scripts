#!/usr/bin/python3
import board
import busio
import adafruit_bme280
import time

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.mode = adafruit_bme280.MODE_NORMAL
#bme280.mode = adafruit_bme280.MODE_FORCE
time.sleep(1)

print("Temperature: %0.1f C" % bme280.temperature)
print("Humidity: %0.1f %%" % bme280.humidity)
print("relative Humidity: %0.1f %%" % bme280.relative_humidity)
print("absolute Pressure: %0.1f hPa" % bme280.pressure)
print("Altitude = %0.2f meters" % bme280.altitude)

