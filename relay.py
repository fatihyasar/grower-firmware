import time
import grovepi

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND

grovepi.pinMode(2,"OUTPUT")
grovepi.pinMode(3,"OUTPUT")
grovepi.pinMode(4,"OUTPUT")
grovepi.pinMode(5,"OUTPUT")
grovepi.pinMode(6,"OUTPUT")
grovepi.pinMode(7,"OUTPUT")

def open(relayNumber):
    grovepi.digitalWrite(relayNumber,1)
    time.sleep(2)
    print (relayNumber, ".relay turned on " )


def close(relayNumber):
    grovepi.digitalWrite(relayNumber,0)
    time.sleep(2)
    print (relayNumber, ".relay turned off " )


########################
# Main
########################

if "__main__" == __name__:
    print "running console mode"
    for x in range(2, 8):
        open(x)
        close(x)    
    quit()
