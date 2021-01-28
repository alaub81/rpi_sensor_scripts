#!/bin/bash

echo "scale=3; $(grep 't=' /sys/bus/w1/devices/w1_bus_master1/28-01142f7ba71a/w1_slave | awk -F't=' '{print $2}')/1000" | bc -l
