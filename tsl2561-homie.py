#!/usr/bin/python3
# Import required Python libraries
import paho.mqtt.client as mqtt
import time, ssl, systemd.daemon
import board
import adafruit_tsl2561

# set the variables
broker = "FQDN / IP ADDRESS"
port = 8883
mqttclientid = "clientid-tsl2561-homie"
clientid = "clientid-tsl2561"
clientname = "Clientname TSL2561 Sensor"
nodes="tsl2561"
username = "mosquitto"
password = "password"
insecure = True
qos = 1
retain_message = True
# Retry to connect to mqtt broker
mqttretry = 5
# how often should be a publish to MQTT (in Seconds)
publishtime=15

# do the stuff
### Functions
def publish(topic, payload):
  client.publish("homie/" + clientid + "/" + topic,payload,qos,retain_message)

def on_connect(client, userdata, flags, rc):
  print("MQTT Connection established, Returned code=",rc)
  # homie client config
  publish("$state","init")
  publish("$homie","4.0")
  publish("$name",clientname)
  publish("$nodes",nodes)
  # homie node config
  publish(nodes + "/$name","TSL2561 Sensor")
  publish(nodes + "/$properties","lux,broadband,infrared")
  publish(nodes + "/lux/$name","Lux")
  publish(nodes + "/lux/$unit","lux")
  publish(nodes + "/lux/$datatype","float")
  publish(nodes + "/lux/$settable","false")
  publish(nodes + "/broadband/$name","Broadband")
  publish(nodes + "/broadband/$datatype","integer")
  publish(nodes + "/broadband/$settable","false")
  publish(nodes + "/infrared/$name","Infrared")
  publish(nodes + "/infrared/$datatype","integer")
  publish(nodes + "/infrared/$settable","false")
  # homie stae ready
  publish("$state","ready")

def on_disconnect(client, userdata, rc):
  print("MQTT Connection disconnected, Returned code=",rc)

def sensorpublish():
  publish(nodes + "/lux","{}".format(sensor.lux))
  publish(nodes + "/broadband","{}".format(sensor.broadband))
  publish(nodes + "/infrared","{}".format(sensor.infrared))

# running the Script
#MQTT Connection
mqttattempts = 0
while mqttattempts < mqttretry:
  try:
    client=mqtt.Client(mqttclientid)
    client.username_pw_set(username, password)
    client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
    client.tls_insecure_set(insecure)
    client.will_set("homie/" + clientid + "/$state","lost",qos,retain_message)
    client.connect(broker, port)
    client.loop_start()
    mqttattempts = mqttretry
  except :
    print("Could not establish MQTT Connection! Try again " + str(mqttretry - mqttattempts) + "x times")
    mqttattempts += 1
    if mqttattempts == mqttretry:
      print("Could not connect to MQTT Broker! exit...")
      exit (0)
    time.sleep(5)

# Tell systemd that our service is ready
systemd.daemon.notify('READY=1')

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# finaly the loop
while True:
  try:
    i2c = board.I2C()
    sensor = adafruit_tsl2561.TSL2561(i2c)
    # Set high gain mode.
    # 0 is low gain 1 is high gain
    sensor.gain = 1
    # Set integration time.
    # A value 0 is 13.7ms, 1 is 101ms, 2 is 402ms, and 3 is manual mode.
    sensor.integration_time = 1
    # publishing the stuff
    sensorpublish()
    time.sleep(publishtime)

  except KeyboardInterrupt:
    print("Goodbye!")
    # At least close MQTT Connection
    publish("$state","disconnected")
    time.sleep(1)
    client.disconnect()
    client.loop_stop()
    exit (0)

# At least close MQTT Connection
print("Script stopped")
publish("$state","disconnected")
time.sleep(1)
client.disconnect()
client.loop_stop()
