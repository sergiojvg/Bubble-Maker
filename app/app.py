#!/bin/python
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("==> RPI.GPIO library not found. Make sure to run this app with -t flag")

#from pynput.keyboard import Key, Listener, KeyCode
#import curses
from sshkeyboard import listen_keyboard
import time
import getopt, sys

class submarine:
    def __init__(self):
        LEFT_FORWARD = 16
        LEFT_BACKWARD = 18
        self.pins = {
            "leftForward": LEFT_FORWARD,
            "leftBackward": LEFT_BACKWARD
        }

        if dry_run == False:
            GPIO.setmode(GPIO.BOARD)
            for pin in pins.values():
                GPIO.setup(pin, GPIO.OUT)
                #GPIO.output(pin, False)
        else:
            self.pinsMocker = {}
            for pin in self.pins.keys():
                self.pinsMocker[pin] = False
            print("- Pins Mocker initialized with values: " + str(self.pinsMocker))

        self.reset()
        #for pin in [leftPin]:
        #    GPIO.setup(pin, GPIO.OUT)

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

    def stopTurnRight(self):
        self.setPin(pinName="leftForward",value=False)

    def startTurnLeft(self):
        self.setPin(pinName="leftBackward",value=True)

    def stopTurnLeft(self):
        self.setPin(pinName="leftBackward",value=False)

    def startForward(self):
        self.setPin(pinName="leftForward",value=True)
        self.setPin(pinName="leftBackward",value=True)

    def stopForward(self):
        self.setPin(pinName="leftForward",value=False)
        self.setPin(pinName="leftBackward",value=False)

    def setPin(self, pinName, value):
        if dry_run == False:
            GPIO.output(self.pins[pinName], value)
        else:
            self.pinsMocker[pinName] = value

def key_pressed_sshkeyboard(key):
    if key == "up":
        bubbles.startForward()
    elif key == "left":
        bubbles.startTurnLeft()
    elif key == "right":
        bubbles.startTurnRight()
    elif key == "i":
        bubbles.printConfiguration()
        bubbles.printStatus()
    elif key == "r":
        bubbles.reset()
    elif key == "q":
        return False
    bubbles.printStatus()

#def key_pressed_handler(key):
#    if hasattr(key, 'char'):
#        if key.char == "q":
#            return False
#        elif key.char == "i":
#            bubbles.printConfiguration()
#            bubbles.printStatus()
#    else:
#        if key == Key.esc:
#            return False
#        elif key == Key.up:
#            bubbles.startForward()
#        elif key == Key.left:
#            bubbles.startTurnLeft()
#        elif key == Key.right:
#            bubbles.startTurnRight()
#        bubbles.printStatus()
#
#
#def key_released_handler(key):
#    if key == Key.esc:
#        return False
#    elif key == Key.up:
#        bubbles.stopForward()
#    elif key == Key.left:
#        bubbles.stopTurnLeft()
#    elif key == Key.right:
#        bubbles.stopTurnRight()

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

    listen_keyboard(on_press=key_pressed_sshkeyboard)
    
    #with Listener(
    #        on_press = key_pressed_handler,
    #        on_release = key_released_handler) as listener:
    #    listener.join()

    #screen = curses.initscr()
    #curses.noecho()
    #curses.cbreak()
    #screen.keypad(True)
    #try:
    #    while True:
    #        char = screen.getch()
    #        if char == ord('q'):
    #            break
    #        elif char == ord("i"):
    #            bubbles.printConfiguration()
    #            bubbles.printStatus()
    #        elif char == curses.KEY_RIGHT:
    #            bubbles.startTurnRight()
    #        elif char == curses.KEY_LEFT:
    #            bubbles.startTurnLeft()
    #        elif char == curses.KEY_UP:
    #            bubbles.startForward()
    #finally:
    #    # shut down cleanly
    #    curses.nocbreak()
    #    screen.keypad(0)
    #    curses.echo()
    #    curses.endwin()





