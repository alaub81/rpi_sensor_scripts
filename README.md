# rpi_sensor_scripts
This is just a repository with all my scripts belonging to the raspberry pi and some sensors, I used. These Scripts could be used as standalone or with a systemd service or even with cronjob.

I put in some systemd service files, too.

# Usage
just download the file you need. `*-mqtt` are able to publish the sensor data to a MQTT Broker. The `*-homie` files are publishing the sensor as an Homie MQTT Device. `*.service` files are the systemd service files. You have to copy them to `/etc/systemd/system/`. To activate them just:
```bash
systemd deamon-reload
# to enable it on systemboot
systemctl enable dht22_homie.service
# Start/Stop/Restart Service
systemctl start dht22_homie.service
systemctl stop dht22_homie.service
systemctl restart dht22_homie.service
```

# more details
* https://www.laub-home.de/wiki/Raspberry_Pi_BH1750_Helligkeitssensor
* https://www.laub-home.de/wiki/Raspberry_Pi_TSL2561_Helligkeitssensor
* https://www.laub-home.de/wiki/Raspberry_Pi_DHT22_Temperatur_Sensor
* https://www.laub-home.de/wiki/Raspberry_Pi_BMP180_Luftdruck_Sensor
* https://www.laub-home.de/wiki/Raspberry_Pi_BME280_Luftdruck_Sensor
* https://www.laub-home.de/wiki/Raspberry_Pi_BMP280_Luftdruck_Sensor
* https://www.laub-home.de/wiki/Raspberry_Pi_DS18B20_Temperatur_Sensor
* https://www.laub-home.de/wiki/Raspberry_Pi_BME680_Gas_Sensor
