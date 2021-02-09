#!/usr/bin/python3

# Import required Python libraries
import paho.mqtt.client as mqtt
import board
import adafruit_tsl2561
import time
import ssl

# set the variables
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-tsl2561"
clientid='python-mqtt-tsl2561'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# define BH1750
i2c = board.I2C()
sensor = adafruit_tsl2561.TSL2561(i2c)
# Set high gain mode.
# 0 is low gain 1 is high gain
sensor.gain = 1
# Set integration time.
# A value 0 is 13.7ms, 1 is 101ms, 2 is 402ms, and 3 is manual mode.
sensor.integration_time = 2

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

#print('Lux: {}'.format(sensor.lux))
#print('Broadband: {}'.format(sensor.broadband))
#print('Infrared: {}'.format(sensor.infrared))
#print('Luminosity: {}'.format(sensor.luminosity))
lux = sensor.lux
if lux == None:
  lux = 0
client.publish("{}/lux".format(publish_topic),"{}".format(lux),qos,retain_message)
client.publish("{}/broadband".format(publish_topic),"{}".format(sensor.broadband),qos,retain_message)
client.publish("{}/infrared".format(publish_topic),"{}".format(sensor.infrared),qos,retain_message)
client.publish("{}/luminosity".format(publish_topic),"{}".format(sensor.luminosity),qos,retain_message)

time.sleep(2)
client.disconnect()
client.loop_stop()

