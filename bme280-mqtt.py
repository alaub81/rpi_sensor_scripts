#!/usr/bin/python3
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import paho.mqtt.client as mqtt
import ssl
import time

# set the variables
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-bme280"
clientid='python-mqtt-bme280'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# define BME280 Sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# change this to match the location's pressure (hPa) at sea level
#bme280.sea_level_pressure = 1010
bme280.mode = adafruit_bme280.MODE_NORMAL
time.sleep(1)

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

client.publish("{}/temperature".format(publish_topic),"{:.2f}".format(bme280.temperature),qos,retain_message)
client.publish("{}/humidity".format(publish_topic),"{:.2f}".format(bme280.humidity),qos,retain_message)
client.publish("{}/pressure".format(publish_topic),"{:.2f}".format(bme280.pressure),qos,retain_message)
client.publish("{}/altitude".format(publish_topic),"{:.2f}".format(bme280.altitude),qos,retain_message)
client.publish("{}/sealevelpressure".format(publish_topic),"{:.2f}".format(bme280.sea_level_pressure),qos,retain_message)

ctime.sleep(1)
client.disconnect()
client.loop_stop()
