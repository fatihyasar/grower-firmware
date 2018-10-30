import temp
import ec
import time

temperatureData = temp.readTempSensor()
print temperatureData

time.sleep(0.1)

ecData = ec.readEC()
print ecData

