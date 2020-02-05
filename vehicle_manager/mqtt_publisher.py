# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
from struct import *
# publish.single("CoreElectronics/test", "Hello", hostname="test.mosquitto.org")
# publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")
# publish.single("CoreElectronics/test", "Hello", hostname="192.168.137.1")
# publish.single("CoreElectronics/topic", "World!", hostname="192.168.137.1")
# print("Done")

def updateSpeed(speed):
    publish.single('VehicleData/speed', pack('f',speed), hostname='192.168.137.1')