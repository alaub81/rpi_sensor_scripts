#!/usr/bin/python3

import time
import board
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

while True:
    try:
        print("Distance: %.2f cm" % sonar.distance)
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)
