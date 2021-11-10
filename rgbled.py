#!/usr/bin/python3
# Import required Python libraries
import RPi.GPIO as GPIO
import time

# Set the Variables
# set red,green and blue pins
redPin = 22
greenPin = 27
bluePin = 17

# Configuration
# disable warnings (optional)
GPIO.setwarnings(False)
# Select GPIO Mode
GPIO.setmode(GPIO.BCM)
# set pins as outputs
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

# Functions
def turnOff():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
def white():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)
def red():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.LOW)
def green():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.LOW)
def blue():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.HIGH)
def yellow():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.LOW)
def purple():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.HIGH)
def lightBlue():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)

# do the stuff
while True:
  try:
    print("Press CTRL+C to exit")
    turnOff()
    time.sleep(1)
    white()
    time.sleep(1)
    red()
    time.sleep(1)
    green()
    time.sleep(1)
    blue()
    time.sleep(1)
    yellow()
    time.sleep(1)
    purple()
    time.sleep(1)
    lightBlue()
    time.sleep(1)
  except KeyboardInterrupt:
    print("Goodbye!")
    turnOff()
    exit (0)
  except :
    print("An Error accured ... ")
    time.sleep(1)
    continue
