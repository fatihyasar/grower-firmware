import grove_i2c_motor_driver
import time

m = grove_i2c_motor_driver.motor_driver(address=0x0a)
# controller2 = grove_i2c_motor_driver.motor_driver(address=0x0a)
try:
        # You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)

        #FORWARD
        print("Forward")
        m.MotorSpeedSetAB(100,0) #defines the speed of motor 1 and motor 2;
        m.MotorDirectionSet(0b1010)     #"0b1010" defines the output polarity, "10" means the M+ is "positive" while the$
        time.sleep(10)

except IOError:
        print("Unable to find the motor driver, check the addrees and press reset on the motor driver and try again")

