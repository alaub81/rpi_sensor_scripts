#!/usr/bin/python3

# Import required Python libraries
import paho.mqtt.client as mqtt
import adafruit_dht
import time
import ssl

# set the variables
dht22gpiopin='D17'
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-dht22"
clientid='python-mqtt-dht22'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# Initial the dht device, with data pin connected to:
dhtboard = getattr(board, dht22gpiopin)

# Standard 
#dhtDevice = adafruit_dht.DHT22(dhtboard)

# you can pass DHT 22 use_pulseio=False if you don't want to use pulseio
# this may be necessary on the Pi zero but will not work in
# circuit python
dhtDevice = adafruit_dht.DHT22(dhtboard, use_pulseio=False)

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

try:
  temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
  client.publish("{}/temperature".format(publish_topic),"{:.1f}".format(temperature),qos,retain_message)
  client.publish("{}/humidity".format(publish_topic),"{}".format(humidity),qos,retain_message)
except RuntimeError as error:
  print(error.args[0])
  time.sleep(5)
  temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
  client.publish("{}/temperature".format(publish_topic),"{:.1f}".format(temperature),qos,retain_message)
  client.publish("{}/humidity".format(publish_topic),"{}".format(humidity),qos,retain_message)

time.sleep(1)
client.disconnect()
client.loop_stop()
