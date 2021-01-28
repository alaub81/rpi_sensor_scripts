#!/usr/bin/python3
import board
import busio
import adafruit_bmp280
import paho.mqtt.client as mqtt
import ssl

# set the variables
broker='FQDN / IP Adresse'
port=8883
publish_topic="house/pi-bmp280"
clientid='python-mqtt-bmp280'
username='mosquitto'
password='password'
insecure=True
qos=1
retain_message=True

# do the stuff
# define BMP280 Sensor
i2c = busio.I2C(board.D27, board.D17)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# change this to match the location's pressure (hPa) at sea level
#bmp280.sea_level_pressure = 1010

#MQTT Connection
client=mqtt.Client(clientid)
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE) #no client certificate needed
client.tls_insecure_set(insecure)
client.connect(broker, port)
client.loop_start()

client.publish("{}/temperature".format(publish_topic),"{:.2f}".format(bmp280.temperature),qos,retain_message)
client.publish("{}/pressure".format(publish_topic),"{:.2f}".format(bmp280.pressure),qos,retain_message)
client.publish("{}/altitude".format(publish_topic),"{:.2f}".format(bmp280.altitude),qos,retain_message)

client.disconnect()
client.loop_stop()
