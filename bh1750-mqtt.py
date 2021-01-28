#!/usr/bin/python3

# Import required Python libraries
import paho.mqtt.client as mqtt
import board
import adafruit_bh1750
import time
import ssl

time.sleep(25)

# set the variables
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-bh1750"
clientid='python-mqtt-bh1750'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# define BH1750
i2c = board.I2C()
lightsensor = adafruit_bh1750.BH1750(i2c)

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

#print("%.2f Lux" % lightsensor.lux)
client.publish("{}/lux".format(publish_topic),"{:.2f}".format(lightsensor.lux),qos,retain_message)

time.sleep(2)
client.disconnect()
client.loop_stop()

