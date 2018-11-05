import temp
import ec
import time
import json
import paho.mqtt.client as mqtt
import grovepi

broker_address="192.168.1.55"

waterLevelSensorPin = 15  # A1
grovepi.pinMode(waterLevelSensorPin,"INPUT")

plugsCommandTopic = '/actuators/plugs/command/+/start'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(plugsCommandTopic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #cmd = json.loads(msg.payload)
    print('on_message : ' + msg.payload)
    # print(sensorName+" "+returnState(sensorVoltage))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address) #connect to broker
client.loop_start() #start the loop

while True:
    except IOError:
    print ("Error")
    client.loop_stop() #stop the loop

'''
while True:
    try:

        temperatureData = temp.readTempSensor()
        json_temperatureData = json.dumps(temperatureData)
        #print 'temp :', json_temperatureData
        client.publish("/sensors/temperature", json_temperatureData) 

        time.sleep(0.5)

        ecData = ec.readEC()
        json_ecData = json.dumps(ecData)
        #print 'ec :', json_ecData
        client.publish("/sensors/ec", json_ecData) 

        time.sleep(0.5)

        waterLevelValue = grovepi.analogRead(waterLevelSensorPin)
        waterLevelData = {}
        waterLevelData['read'] = 'success'
        waterLevelData['sensor'] = waterLevelValue;
        waterLevelData['time'] = int(time.time())

        json_WaterLevelData = json.dumps(waterLevelData)
        #print 'water level :', json_WaterLevelData
        client.publish("/sensors/waterlevel", json_WaterLevelData)         
        time.sleep(3)

    except IOError:
        print ("Error")
        client.loop_stop() #stop the loop
'''
