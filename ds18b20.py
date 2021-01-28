#!/usr/bin/python3
import sys

# Path to the Sensor systempath
# 28-01142f7ba71a has to be changed to you sensor path!
sensor = '/sys/bus/w1/devices/28-01142f7ba71a/w1_slave'

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

print("Temperature: " + str(readTempLines(sensor)[0]) + " °C")
print("Temperature: " + str(readTempLines(sensor)[1]) + " K")
print("Temperature: " + str(readTempLines(sensor)[2]) + " °F")
