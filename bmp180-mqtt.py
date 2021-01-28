#!/usr/bin/python3
# Import required Python libraries
import Adafruit_BMP.BMP085 as BMP085
import paho.mqtt.client as mqtt
import time
import ssl

# set the variables
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-bmp180"
clientid='python-mqtt-bmp180'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# define BMP180 Sensor
sensor = BMP085.BMP085()

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

client.publish("{}/temperature".format(publish_topic),"{:.2f}".format(sensor.read_temperature()),qos,retain_message)
client.publish("{}/pressure".format(publish_topic),"{:.2f}".format(sensor.read_pressure()/100),qos,retain_message)
client.publish("{}/altitude".format(publish_topic),"{:.2f}".format(sensor.read_altitude()),qos,retain_message)

client.disconnect()
client.loop_stop()
