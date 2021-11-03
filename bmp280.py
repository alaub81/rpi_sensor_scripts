#!/usr/bin/python3
import board
import busio
import digitalio
import adafruit_bmp280
import time

#i2c = busio.I2C(board.D27, board.D17)
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

print("Temperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.1f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)

"""
bmp280.mode = adafruit_bmp280.MODE_NORMAL
time.sleep(1)

print("Temperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.1f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)

bmp280.mode = adafruit_bmp280.MODE_FORCE
time.sleep(1)

print("Temperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.1f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)

bmp280.mode = adafruit_bmp280.MODE_SLEEP
time.sleep(1)

print("Temperature: %0.1f C" % bmp280.temperature)
print("Pressure: %0.1f hPa" % bmp280.pressure)
print("Altitude = %0.2f meters" % bmp280.altitude)
"""
