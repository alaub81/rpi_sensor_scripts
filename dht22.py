#!/usr/bin/python3
import time, adafruit_dht, board

# set the variable
dht22gpiopin = 'D17'


# Initial the dht device, with data pin connected to:
dhtboard = getattr(board, dht22gpiopin)

# you can pass DHT 22 use_pulseio=False if you don't want to use pulseio
# this may be necessary on the Pi zero but will not work in
# circuit python
dhtDevice = adafruit_dht.DHT22(dhtboard, use_pulseio=False)
# Standard is, but not working on the raspberry pi boards
#dhtDevice = adafruit_dht.DHT22(dhtboard)


try:
  # Print the values to the serial port
  temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
  print("Temperature: {:.1f} °C  Humidity: {:.1f} %".format(temperature, humidity))

except RuntimeError as error:
  # Errors happen fairly often, DHT's are hard to read, just keep going
  time.sleep(2.0)
  # Print the values to the serial port
  temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
  print("Temperature: {:.1f} °C  Humidity: {:.1f} %".format(temperature, humidity))
