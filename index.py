import temp
import ec
import waterlevel
import relay
import time
import json
from sensor import sensor
import grove_i2c_motor_driver
import paho.mqtt.client as mqtt
from threading import Lock, Thread

broker_address = "192.168.1.55"
MQTT_TOPIC = [("/actuators/plugs/command/#",0), ("/actuators/motors/command/#",0)]
motorController = grove_i2c_motor_driver.motor_driver()
lock = Lock() #thread lock

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


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
        #lock.acquire()     
        relay.open(plugNumber)
        client.publish('/sensors/plugs/'+str(plugNumber)+'/state', 'on') 
        print("published : " + '/sensors/plugs/'+str(plugNumber)+'/state')
        #lock.release()     
    except Exception as e:
        #lock.release()     
        raise e



def on_close_plug(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # 
    print("on_close_plug  : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    cmds =  msg.topic.split('/')
    plugNumber = int(cmds[4])    
    try:
        #lock.acquire()     
        relay.close(plugNumber)
        #lock.release()     
    except Exception as e:
        #lock.release()     
        raise e

    client.publish('/sensors/plugs/'+str(plugNumber)+'/state', 'off') 


def on_start_motor(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # 
    # /actuators/motors/[motor number]/start/[dir]/[[speed 0|100]]
    print("on_start_motor message : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    cmds =  msg.topic.split('/')
    motorNumber = int(cmds[3])
    direction = int(cmds[5])
    speed = int(cmds[6])

    try:
        sens = sensList.getSensor(motorNumber)
        sens.state = "running"
        sens.direction = direction
        if sens.direction == 1:  
            motorController.MotorDirectionSet(0b1010)
            print("motor set to forward");
        elif sens.direction == 0: 
            motorController.MotorDirectionSet(0b0101)
            print("motor set to backward");

        sens.speed = abs(speed)

        print("motor configuration updated")

        #fy: assign later. other motorcontroller according to controllerNumber
        motorController.MotorSpeedSetAB(speed,0) #defines the speed of motor 1 and motor 2;
        lock.release()
    except Exception as e:
        lock.release()
        raise e

    publishState(sens.sensorID, sens.state, sens.speed, sens.direction)


def publishState(motorNumber, state, speed, direction):
    topicState = "/actuators/motors/" + str(motorNumber) + "/state"
    topicSpeed = "/actuators/motors/" + str(motorNumber) + "/speed"
    topicDirection = "/actuators/motors/" + str(motorNumber) + "/direction"
    
    client.publish(topicState, state)
    client.publish(topicSpeed, str(speed))
    client.publish(topicDirection, str(direction))


def on_stop_motor(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # /actuators/motors/+/stop
    cmds =  msg.topic.split('/')
    motorNumber = int(cmds[3])
    stopMotor(motorNumber)
    print("on_stop_motor message : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def stopMotor(motorNumber):
    print("stopping motor", motorNumber)
    sens = sensList.getSensor(motorNumber)
    sens.state = "stopped"
    sens.speed = 0
    sens.direction = -1
    motorController.MotorSpeedSetAB(0,0) 
    publishState(sens.sensorID, sens.state, sens.speed, sens.direction)


class sensorList():
    	def __init__(self):
		self.sensorList = {}
 
	def addSensor(self, sensorName, humanName, sensorID):
		self.sensorList[sensorID] = sensor()
		self.sensorList[sensorID].setname(sensorName, humanName, sensorID)
		self.sensorList[sensorID].setState("ready")
 
	def getSensorName(self, sensorID):
		return self.sensorList[sensorID].getname()
 
	def getSensor(self, sensorID):
    		return self.sensorList[sensorID]

	def sensorState(self, sensorID, monitorState):
             self.sensorList[sensorID].state = monitorState



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add("/actuators/plugs/command/+/on", on_open_plug)
client.message_callback_add("/actuators/plugs/command/+/off", on_close_plug)
client.message_callback_add("/actuators/motors/command/+/start/+/+", on_start_motor)
client.message_callback_add("/actuators/motors/command/+/stop", on_stop_motor)

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

        #ecData = ec.readEC()
        #json_ecData = json.dumps(ecData)
        #print 'ec :', json_ecData
        #client.publish("/sensors/ec", json_ecData) 

        #time.sleep(0.5)

        #waterLevelData = waterlevel.readWaterLevel()
        #json_WaterLevelData = json.dumps(waterLevelData)
        #print 'water level :', json_WaterLevelData
        #client.publish("/sensors/waterlevel", json_WaterLevelData)         
        time.sleep(3)
        lock.release()
    except IOError:
        print ("Error")
        lock.release()
        client.loop_stop() #stop the loop

