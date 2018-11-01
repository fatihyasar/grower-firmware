import temp
import ec
import time
import json
import paho.mqtt.client as mqtt

broker_address="192.168.1.55"

client = mqtt.Client("P1")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop

while True:
    try:

        temperatureData = temp.readTempSensor()
        json_temperatureData = json.dumps(temperatureData)
        print 'temp data :', json_temperatureData
        client.publish("/sensors/temperature", json_temperatureData) 

        time.sleep(0.5)

        ecData = ec.readEC()
        json_ecData = json.dumps(ecData)
        print 'ec data :', json_ecData
        client.publish("/sensors/ec", json_ecData) 

        time.sleep(3)

    except IOError:
        print ("Error")
        client.loop_stop() #stop the loop
