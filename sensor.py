
class sensor():
    	def __init__(self):
		self.name = ""       	        # Name of sensor in MQTT
		self.sensorID = 0
		self.humanName = ""	  			# Human-meaningful name (e.g., "front door")
		self.lastSeen = 0	            # Number of seconds since the sensor was last seen
		self.state = "unknown"	        # State of the object: unknown, open, or closed
		self.speed = 0
		self.direction = -1

	def setState(self, newstate):
		self.state = newstate
 
	def getState(self):
		return self.state
 
	def resetHeartbeat(self):
		self.lastSeen = 0
 
	def setname(self, newName, humanName, sensorID):
		self.name = newName
		self.sensorID = sensorID 
		self.humanName = humanName
 
	def getname(self):
		return self.humanName
 
	def checkState(self, newState):
    		self.state = newState
