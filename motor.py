########################
# Libraries
########################
import os
import string
import paho.mqtt.client as mqtt
import time
import json
import threading
from sensor import sensor
import grove_i2c_motor_driver

########################
# Globals
########################

localBroker = "192.168.1.55"		        # Local MQTT broker m2m.eclipse.org
localPort = 1883			                # Local MQTT port
localUser = ""              		        # Local MQTT user
localPass = ""	                            # Local MQTT password
deviceTopic = "/actuators/motors/#"		    # Local MQTT topic to monitor
localTimeOut = 120			                # Local MQTT session timeout
sensorList = {}
motorController = grove_i2c_motor_driver.motor_driver()

global motorSpeed1 
global motorSpeed2
global motorSpeed3
global motorSpeed4


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(deviceTopic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #cmd = json.loads(msg.payload)

    print('>>> on_message : ' + msg.payload)
    # print(sensorName+" "+returnState(sensorVoltage))


def on_start_motor(mosq, obj, msg):
    # This callback will only be called for messages with topics that match
    # 
    # /actuators/motors/[motor number]/start/[dir]/[[speed 0|100]]/[runforsec 0 = not use| x seconds]
    print("on_start_motor message : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    cmds =  msg.topic.split('/')
    motorNumber = int(cmds[3])
    direction = int(cmds[5])
    speed = int(cmds[6])
    runforsec = int(cmds[7])

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

    print("motor configuration updated for motorNumber : " + str(motorNumber))

    if motorNumber == 1:
        motorSpeed1 = speed
    if motorNumber == 2:
        motorSpeed2 = speed

    motorController.MotorSpeedSetAB(motorSpeed1, motorSpeed2) 
    publishState(sens.sensorID, sens.state, sens.speed, sens.direction)

    if runforsec > 0:                 
        timer = threading.Timer(runforsec, stopMotor, [motorNumber])
        timer.start()   



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

    if motorNumber == 1:
        motorSpeed1 = 0
    if motorNumber == 2:
        motorSpeed2 = 0

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



########################
# Main
########################
 
if "__main__" == __name__:
        sensList = sensorList()
        sensList.addSensor("M1", "Motor1", 1)
        sensList.addSensor("M2", "Motor2", 2)
        sensList.addSensor("M3", "Motor3", 3)
        sensList.addSensor("M4", "Motor4", 4)
    
    
        client = mqtt.Client()
        client.on_connect = on_connect


        #subscribe generic motor channel
        client.message_callback_add("/actuators/motors/+/start/+/+/+", on_start_motor)
        client.message_callback_add("/actuators/motors/+/stop", on_stop_motor)
        client.on_message = on_message
    
        client.connect(localBroker, localPort, localTimeOut)
    
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()
    
        quit()


