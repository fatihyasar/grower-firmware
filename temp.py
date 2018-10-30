import grovepi
import math
import json
import time
import paho.mqtt.client as mqtt

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
# sensor = 4  # The Sensor goes on digital port 4.
#broker_address="192.168.1.55"

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
# blue = 0    # The Blue colored sensor.
# white = 1   # The White colored sensor.
# mqttPath = "/sensors/temperature"
# tempData = {}

# print time.time()
# client = mqtt.Client("P1")
# client.connect(broker_address) #connect to broker
# client.loop_start() #start the loop

def readTempSensor():
    # This example uses the blue colored sensor. 
    # The first parameter is the port, the second parameter is the type of sensor.
    [temp,humidity] = grovepi.dht(4, 1)  # sensor pin, white = 1  | blue = 0 
    tempData = {}
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        tempData['read'] = "success"
        tempData['temp'] = temp
        tempData['humidity'] = humidity
        tempData['time'] = int(time.time())
        #print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        #json_data = json.dumps(data)
        #print('data', json_data)
        #client.publish(mqttPath, json_data) 
    else:
        tempData['read'] = "fail"
    return tempData 