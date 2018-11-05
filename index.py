import temp
import ec
import time
import json
import paho.mqtt.client as mqtt
import grovepi

broker_address="192.168.1.55"

waterLevelSensorPin = 15  # A1
grovepi.pinMode(waterLevelSensorPin,"INPUT")

plugsCommandTopic = '/actuators/plugs/command'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(plugsCommandTopic1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #cmd = json.loads(msg.payload)

    print('on_message : ' + msg)
    # print(sensorName+" "+returnState(sensorVoltage))


def on_start_plug(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # /actuators/motors/+/stop
    cmds =  msg.topic.split('/')
    motorNumber = int(cmds[3])
    stopMotor(motorNumber)
    print("on_stop_motor message : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_stop_plug(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # /actuators/motors/+/stop
    cmds =  msg.topic.split('/')
    motorNumber = int(cmds[3])
    stopMotor(motorNumber)
    print("on_stop_motor message : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("/actuators/plugs/command/+/start", on_start_plug)
client.message_callback_add("/actuators/plugs/command/+/stop", on_stop_plug)


client.connect(broker_address) #connect to broker
client.loop_start() #start the loop


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
