#!/usr/bin/python3
import Adafruit_DHT

gpiopin=17

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, gpiopin)
print("Temperature: {:.1f} °C  Humidity: {:.1f} %".format(temperature, humidity))
