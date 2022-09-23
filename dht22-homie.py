#!/usr/bin/python3
# Import required Python libraries
import paho.mqtt.client as mqtt
import adafruit_dht
import board, time, ssl, systemd.daemon

# set the variables
dht22gpiopin = "D17"
broker = "FQDN / IP ADDRESS"
port = 8883
mqttclientid = "clientid-dht22-homie"
clientid = "clientid-dht22"
clientname = "Clientname DHT22 Sensor"
nodes = "dht22"
username = "mosquitto"
password = "password"
insecure = True
qos = 1
retain_message = True
# Retry to connect to mqtt broker
mqttretry = 5
# how often should be a publish to MQTT (in Seconds)
publishtime = 120
# At which value humidity alarm will be fired (x in %)
humidityalarm = 70

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
  publish(nodes + "/$name","DHT22 Sensor")
  publish(nodes + "/$properties","temperature,humidity")
  publish(nodes + "/temperature/$name","Temperature")
  publish(nodes + "/temperature/$unit","°C")
  publish(nodes + "/temperature/$datatype","float")
  publish(nodes + "/temperature/$settable","false")
  publish(nodes + "/humidity/$name","Humidity")
  publish(nodes + "/humidity/$unit","%")
  publish(nodes + "/humidity/$datatype","float")
  publish(nodes + "/humidity/$settable","false")
  publish(nodes + "/humidityalarm/$name", "Humidity Alarm")
  publish(nodes + "/humidityalarm/$datatype", "boolean")
  publish(nodes + "/humidityalarm/$settable", "false")
  # homie stae ready
  publish("$state","ready")

def on_disconnect(client, userdata, rc):
  print("MQTT Connection disconnected, Returned code=",rc)

def sensorpublish():
  publish(nodes + "/temperature","{:.1f}".format(temperature))
  publish(nodes + "/humidity","{:.1f}".format(humidity))
  if humidity >= humidityalarm:
    publish(nodes + "/humidityalarm", "true")
  else:
    publish(nodes + "/humidityalarm", "false")

# running the Script
# Initial the dht device, with data pin connected to:
dhtboard = getattr(board, dht22gpiopin)

# Standard 
#dhtDevice = adafruit_dht.DHT22(dhtboard)

# you can pass DHT 22 use_pulseio=False if you don't want to use pulseio
# this may be necessary on the Pi zero but will not work in
# circuit python
dhtDevice = adafruit_dht.DHT22(dhtboard, use_pulseio=False)
time.sleep(1)

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
    temperature, humidity = dhtDevice.temperature, dhtDevice.humidity
    #print(temperature, humidity)
    if humidity <= 100:
      sensorpublish()
      time.sleep(publishtime)
      #print(temperature, humidity)
    time.sleep(3)

  except RuntimeError as error:
    print(error.args[0])
    time.sleep(5)
    continue

  except KeyboardInterrupt:
    print("Goodbye!")
    # At least close MQTT Connection
    publish("$state","disconnected")
    time.sleep(1)
    client.disconnect()
    client.loop_stop()
    exit (0)

  except :
    print("An Error accured ... ")
    time.sleep(3)
    continue

# At least close MQTT Connection
print("Script stopped")
publish("$state","disconnected")
time.sleep(1)
client.disconnect()
client.loop_stop()
