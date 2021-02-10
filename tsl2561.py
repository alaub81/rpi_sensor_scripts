#!/usr/bin/python3
import board
import adafruit_tsl2561

i2c = board.I2C()
sensor = adafruit_tsl2561.TSL2561(i2c)

# Set high gain mode.
# 0 is low gain 1 is high gain
sensor.gain = 0
# Set integration time.
# A value 0 is 13.7ms, 1 is 101ms, 2 is 402ms, and 3 is manual mode.
sensor.integration_time = 0

print('Lux: {}'.format(sensor.lux))
print('Broadband: {}'.format(sensor.broadband))
print('Infrared: {}'.format(sensor.infrared))
print('Luminosity: {}'.format(sensor.luminosity))
