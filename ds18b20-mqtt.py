#!/usr/bin/python3
import sys
import paho.mqtt.client as mqtt
import ssl
 
# set the variables
# Path to the Sensor systempath
# 28-01142f7ba71a has to be changed to you sensor path!
sensor = '/sys/bus/w1/devices/28-01142f7ba71a/w1_slave'
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-ds18b20"
clientid='python-mqtt-ds18b20'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
def readTempSensor(sensorName) :
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000.0
        tempKelvin = 273 + float(tempData) / 1000
        tempFahrenheit = float(tempData) / 1000 * 9.0 / 5.0 + 32.0
        return [tempCelsius, tempKelvin, tempFahrenheit]

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

client.publish("{}/temperature".format(publish_topic),"{:.2f}".format(readTempLines(sensor)[0]),qos,retain_message)

client.disconnect()
client.loop_stop()
