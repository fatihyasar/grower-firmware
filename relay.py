import time
import grovepi

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND

grovepi.pinMode(relay,"OUTPUT")

def open(relayNumber):
    grovepi.digitalWrite(relayNumber,1)
    time.sleep(2)
    print ("on")


def close(relayNumber):
    grovepi.digitalWrite(relayNumber,0)
    time.sleep(2)
    print ("off")


########################
# Main
########################

if "__main__" == __name__:
    for x in range(2, 7):
        open(x)
        close(x)    
    quit()
