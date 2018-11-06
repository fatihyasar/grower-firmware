import time
import grovepi

# Connect the Grove Relay to digital port D4
# SIG,NC,VCC,GND
relay = 4

grovepi.pinMode(relay,"OUTPUT")

def open(relayNumber):
    grovepi.digitalWrite(relay,1)
    time.sleep(2)
    print ("on")


def close(relayNumber):
    grovepi.digitalWrite(relay,0)
    time.sleep(2)
    print ("off")


########################
# Main
########################

if "__main__" == __name__:
        open(1)
        close(1)    
        open(1)
        close(1)    
        quit()
