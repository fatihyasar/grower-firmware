import temp
import ec
import waterlevel
import relay
import time
import json
import paho.mqtt.client as mqtt
from threading import Lock, Thread

broker_address = "192.168.1.55"
plugsCommandTopic = '/actuators/plugs/command/#'

lock = Lock() #thread lock

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


def on_open_plug(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # 
    print("on_open_plug  : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    cmds =  msg.topic.split('/')
    plugNumber = int(cmds[4])

    try:
        lock.acquire()     
        relay.open(plugNumber)
        lock.release()     
    except Exception as e:
        lock.release()     
        raise e

    client.publish('/sensors/plugs/'+str(plugNumber)+'/state', 'on') 



def on_close_plug(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # 
    print("on_close_plug  : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    cmds =  msg.topic.split('/')
    plugNumber = int(cmds[4])    
    try:
        lock.acquire()     
        relay.close(plugNumber)
        lock.release()     
    except Exception as e:
        lock.release()     
        raise e

    client.publish('/sensors/plugs/'+str(plugNumber)+'/state', 'off') 



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("/actuators/plugs/command/+/on", on_open_plug)
client.message_callback_add("/actuators/plugs/command/+/off", on_close_plug)

client.connect(broker_address) #connect to broker
client.loop_start() #start the loop


while True:
    try:
        lock.acquire()        
        temperatureData = temp.readTempSensor()
        json_temperatureData = json.dumps(temperatureData)
        temperatureData = temp.readTempSensor()
        print 'temp :', json_temperatureData
        client.publish("/sensors/temperature", json_temperatureData) 

        time.sleep(0.5)

        #ecData = ec.readEC()
        #json_ecData = json.dumps(ecData)
        #print 'ec :', json_ecData
        #client.publish("/sensors/ec", json_ecData) 

        #time.sleep(0.5)

        waterLevelData = waterlevel.readWaterLevel()
        json_WaterLevelData = json.dumps(waterLevelData)
        print 'water level :', json_WaterLevelData
        client.publish("/sensors/waterlevel", json_WaterLevelData)         
        time.sleep(3)
        lock.release()
    except IOError:
        print ("Error")
        lock.release()
        client.loop_stop() #stop the loop

