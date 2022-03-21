#!/bin/python
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("==> RPI.GPIO library not found. Make sure to run this app with -t flag")

from sshkeyboard import listen_keyboard
import time
import getopt, sys

class submarine:
    def __init__(self):
        LEFT_FORWARD = 16
        LEFT_BACKWARD = 18
        RIGHT_FORWARD = 11
        RIGHT_BACKWARD = 13
        UP = 29
        DOWN = 31
        self.pins = {
            "leftForward": LEFT_FORWARD,
            "leftBackward": LEFT_BACKWARD,
            "rightForward": RIGHT_FORWARD,
            "rightBackward": RIGHT_BACKWARD,
            "up": UP,
            "down": DOWN
        }

        if dry_run == False:
            GPIO.setmode(GPIO.BOARD)
            for pin in self.pins.values():
                GPIO.setup(pin, GPIO.OUT)
        else:
            self.pinsMocker = {}
            for pin in self.pins.keys():
                self.pinsMocker[pin] = False
            print("- Pins Mocker initialized with values: " + str(self.pinsMocker))

        self.reset()

    def reset(self):
      for pinName in self.pins.keys():
          self.setPin(pinName=pinName,value=False)

    def printConfiguration(self):
        print("=> Submarine config:")
        for pinName in self.pins.keys():
            print("---- Pin for " + pinName + " is configured on pin number " + str(self.pins[pinName]) )

    def printStatus(self):
        if dry_run == True:
            print("Currently, pins are configured like this: ")
            print("- Pins Mocker: " + str(self.pinsMocker))

    def startTurnRight(self):
        self.setPin(pinName="leftForward",value=True)
        self.setPin(pinName="rightBackward",value=True)

    def startTurnLeft(self):
        self.setPin(pinName="leftBackward",value=True)
        self.setPin(pinName="rightForward",value=True)

    def startForward(self):
        self.setPin(pinName="leftForward",value=True)
        self.setPin(pinName="rightForward",value=True)

    def startBackward(self):
        self.setPin(pinName="leftBackward",value=True)
        self.setPin(pinName="rightBackward",value=True)

    def startUp(self):
        self.setPin(pinName="up",value=True)

    def startDown(self):
        self.setPin(pinName="down",value=True)

    def setPin(self, pinName, value):
        if dry_run == False:
            GPIO.output(self.pins[pinName], value)
        else:
            self.pinsMocker[pinName] = value

def key_pressed_sshkeyboard(key):
    if key == "up":
        bubbles.startForward()
    if key == "down":
        bubbles.startBackward()
    elif key == "left":
        bubbles.startTurnLeft()
    elif key == "right":
        bubbles.startTurnRight()
    elif key == "w":
        bubbles.startUp()
    elif key == "s":
        bubbles.startDown()
    elif key == "i":
        bubbles.printConfiguration()
        bubbles.printStatus()
    elif key == "r":
        bubbles.reset()
    elif key == "q":
        return
    bubbles.printStatus()

def key_released_sshkeyboard(key):
    bubbles.printStatus()
    bubbles.reset()
    print("Reset")
    bubbles.printStatus()

if __name__ == "__main__":
    global dry_run
    dry_run = False

    argumentList = sys.argv[1:]
    options = "ht:"
    long_options = ["help", "test"]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
 
            if currentArgument in ("-h", "--help"):
                print ("Displaying Help")
                exit()
                 
            elif currentArgument in ("-t", "--test"):
                print("Running in dry_run mode")
                dry_run = True 
             
    except getopt.error as err:
        print (str(err))

    print("==> Application started")
    print("==> Initializing bubbles")

    bubbles = submarine()
    bubbles.printConfiguration()

    listen_keyboard(
        on_press=key_pressed_sshkeyboard,
        on_release=key_released_sshkeyboard)
    
