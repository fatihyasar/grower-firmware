import os
import string
import paho.mqtt.client as mqtt
import time
import json
import grove_i2c_motor_driver

########################
# Main
######################## 
if "__main__" == __name__:

        motorController1 = grove_i2c_motor_driver.motor_driver(0x0f)
        motorController1.MotorSpeedSetAB(0,0)
        motorController1.MotorDirectionSet(0b1010) 

        #motorController2 = grove_i2c_motor_driver.motor_driver(0x0e)
        #motorController2.MotorSpeedSetAB(100,100)
        #motorController2.MotorDirectionSet(0b1010)
    
        quit()

