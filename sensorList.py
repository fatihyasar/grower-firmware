from sensor import sensor

class sensorList():
    	def __init__(self):
		self.sensorList = {}
 
	def addSensor(self, sensorName, humanName, sensorID):
		self.sensorList[sensorName] = sensor()
		self.sensorList[sensorName].setname(sensorName, humanName, sensorID)
		self.sensorList[sensorName].setState("ready")
 
	def getSensorName(self, sensorID):
		return self.sensorList[sensorID].getname()
 
	def getSensor(self, sensorID):
    		return self.sensorList[sensorID]

	def sensorState(self, sensorID, monitorState):
             self.sensorList[sensorID].state = monitorState
 