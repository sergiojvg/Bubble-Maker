#!/bin/python
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("==> RPI.GPIO library not found. Make sure to run this app with -t flag")

import time
import getopt, sys

class submarine:
    def __init__(self,leftPin):
        self.leftPin = leftPin
        self.pins = {
            "left": leftPin
        }

        if dry_run == False:
            GPIO.setmode(GPIO.BOARD)
            for pin in pins.values():
                GPIO.setup(pin, GPIO.OUT)
        #for pin in [leftPin]:
        #    GPIO.setup(pin, GPIO.OUT)

    def printInformation(self):
        print("=> Submarine config:")
        for pinName in self.pins.keys():
            print("---- Pin for " + pinName + " is configured on pin number " + str(self.pins[pinName]) )


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

    bubbles = submarine(leftPin=16)
    bubbles.printInformation()



