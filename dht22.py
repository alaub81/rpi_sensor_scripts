#!/usr/bin/python3
import time, adafruit_dht, board

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D17)

# you can pass DHT 22 use_pulseio=False if you don't want to use pulseio
# this may be necessary on the Pi zero but will not work in
# circuit python
#dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

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
