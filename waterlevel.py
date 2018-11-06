import time,sys
import RPi.GPIO as GPIO
import smbus
import math
import grovepi

waterLevelSensorPin = 15  # A1
grovepi.pinMode(waterLevelSensorPin,"INPUT")


def readWaterLevel():
    data = grovepi.analogRead(waterLevelSensorPin)
    data = {}
    data['read'] = 'success'
    data['value'] = waterLevelValue;
    data['time'] = int(time.time())
    return data




