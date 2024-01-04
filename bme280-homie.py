#!/usr/bin/python3
# Import required Python libraries
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import paho.mqtt.client as mqtt
import time
import ssl
import systemd.daemon

# set the variables
broker = 'FQDN / IP Adresse'
port = 8883
mqttclientid = "clientid-bme280-homie"
clientid = "clientid-bme280"
clientname = "Clientname BME280 Sensor"
nodes = "bme280"
username = 'mosquitto'
password = 'password'
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
# Functions


def publish(topic, payload):
    client.publish("homie/" + clientid + "/" + topic,
                   payload, qos, retain_message)


def on_connect(client, userdata, flags, rc):
    print("MQTT Connection established, Returned code=", rc)
    # homie client config
    publish("$state", "init")
    publish("$homie", "4.0")
    publish("$name", clientname)
    publish("$nodes", nodes)
    # homie node config
    publish(nodes + "/$name", "BME280 Sensor")
    publish(nodes + "/$properties","temperature,humidity,humidityalarm,pressure")
    publish(nodes + "/temperature/$name", "Temperature")
    publish(nodes + "/temperature/$unit", "°C")
    publish(nodes + "/temperature/$datatype", "float")
    publish(nodes + "/temperature/$settable", "false")
    publish(nodes + "/humidity/$name", "Humidity")
    publish(nodes + "/humidity/$unit", "%")
    publish(nodes + "/humidity/$datatype", "float")
    publish(nodes + "/humidity/$settable", "false")
    publish(nodes + "/humidityalarm/$name", "Humidity Alarm")
    publish(nodes + "/humidityalarm/$datatype", "boolean")
    publish(nodes + "/humidityalarm/$settable", "false")
    publish(nodes + "/pressure/$name", "Pressure")
    publish(nodes + "/pressure/$unit", "hPa")
    publish(nodes + "/pressure/$datatype", "float")
    publish(nodes + "/pressure/$settable", "false")
    # homie stae ready
    publish("$state", "ready")


def on_disconnect(client, userdata, rc):
    print("MQTT Connection disconnected, Returned code=", rc)


# running the Script
# define BME280 Sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
# change this to match the location's pressure (hPa) at sea level
#bme280.sea_level_pressure = 1010
bme280.mode = adafruit_bme280.MODE_NORMAL
time.sleep(1)

# MQTT Connection
mqttattempts = 0
while mqttattempts < mqttretry:
    try:
        client = mqtt.Client(mqttclientid)
        client.username_pw_set(username, password)
        client.tls_set(cert_reqs=ssl.CERT_NONE)  # no client certificate needed
        client.tls_insecure_set(insecure)
        client.will_set("homie/" + clientid + "/$state","lost", qos, retain_message)
        client.connect(broker, port)
        client.loop_start()
        mqttattempts = mqttretry
    except:
        print("Could not establish MQTT Connection! Try again " +
              str(mqttretry - mqttattempts) + "x times")
        mqttattempts += 1
        if mqttattempts == mqttretry:
            print("Could not connect to MQTT Broker! exit...")
            exit(0)
        time.sleep(5)

# Tell systemd that our service is ready
systemd.daemon.notify('READY=1')

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# finaly the loop
while True:
    try:
        humidity = bme280.humidity
        publish(nodes + "/temperature", "{:.2f}".format(bme280.temperature))
        publish(nodes + "/humidity", "{:.2f}".format(humidity))
        publish(nodes + "/pressure", "{:.2f}".format(bme280.pressure))
        if humidity >= humidityalarm:
            publish(nodes + "/humidityalarm", "true")
        else:
            publish(nodes + "/humidityalarm", "false")
        time.sleep(publishtime)

    except KeyboardInterrupt:
        print("Goodbye!")
        # At least close MQTT Connection
        publish("$state", "disconnected")
        time.sleep(1)
        client.disconnect()
        client.loop_stop()
        exit(0)

    except:
        print("An Error accured ... ")
        time.sleep(3)
        continue

# At least close MQTT Connection
print("Script stopped")
publish("$state", "disconnected")
time.sleep(1)
client.disconnect()
client.loop_stop()