import time,sys
import RPi.GPIO as GPIO
import smbus
import math
#import json
#import paho.mqtt.client as mqtt

#broker_address="192.168.1.55"
#mqttPath = "/sensors/ec"
#data = {}

#debug = 1
# use the bus that matches your raspi version

debug = 1
# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

#print time.time()
#client = mqtt.Client("P1")
#client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop

def readEC():
    data = {}
    ADDRESS = 0x12

    #temperature
    bus.write_byte(ADDRESS,0xa6)
    sensorData = bus.read_i2c_block_data(ADDRESS, 0, 2)
    temp=(sensorData[1]&0x0f)<<8 | sensorData[0] 

    #humudity
    bus.write_byte(ADDRESS,0xa7)
    sensorData = None
    sensorData = bus.read_i2c_block_data(ADDRESS, 0, 2)
    humudity=(sensorData[1]&0x0f)<<8 | sensorData[0]

    #Dielectric
    bus.write_byte(ADDRESS,0xa8)
    sensorData = None
    sensorData = bus.read_i2c_block_data(ADDRESS, 0, 2)
    dielectric=(sensorData[1]&0x0f)<<8 | sensorData[0]

    #EC
    bus.write_byte(ADDRESS,0xa9)
    sensorData = None
    sensorData = bus.read_i2c_block_data(ADDRESS, 0, 2)
    ec=(sensorData[1]&0x0f)<<8 | sensorData[0]

    #print "Water Temp :", temp / 100, " -EC :", ec / 1000
    data['read'] = "success"
    data['ec'] =  ec / 1000
    data['water_temp'] = temp / 100
    data['time'] = int(time.time())
    # json_data = json.dumps(data)
    # print 'data :', json_data
    # client.publish(mqttPath, json_data) 
    # time.sleep(3)
    return data




