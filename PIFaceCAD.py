#!/usr/bin/python

# PIFaceCAD.py
# Crude wrapper thing so we can call the PIFaceCAD stuff from nodered
# cwhite
# Decemeber 2014

# Import libs - TODO: check pfc is installed!

import sys
import pifacecad

def handleButtonPress(event):
    print('press ' + str(event.pin_num) )


def listenForButtonPresses():
    global pressListenerActive
    for i in range(8):
        pressListener.register(i, pifacecad.IODIR_FALLING_EDGE, handleButtonPress)
    pressListener.activate()
    pressListenerActive = True

def ignoreButtonPresses():
    global pressListenerActive
    if pressListenerActive == True:
        pressListener.deactivate()
        pressListenerActive = False





def handleButtonRelease(event):
    print('release ' + str(event.pin_num) )


def listenForButtonReleases():
    global releaseListenerActive
    for i in range(8):
        releaseListener.register(i, pifacecad.IODIR_RISING_EDGE, handleButtonRelease)
    releaseListener.activate()
    releaseListenerActive = True

def ignoreButtonReleases():
    global releaseListenerActive
    if releaseListenerActive == True:
        releaseListener.deactivate()
        releaseListenerActive = False




def badParams():
    print( "Bad parameters - {disp|clear|blink|move|light|press|release|persist} {str|left|right|on|off|num}")


# process the command we got. Set True if we are persistant... this might help prevent unintentionally recursing
def dispatch(isCalledFromPersist, cmd):
    #print( 'Argument List:', str(sys.argv))
    
    if isCalledFromPersist==True:
        # tweak what we have so it 'matches' what things are like if we are called in a non-persistent way
        if len(cmd) < 1:
            cmd = "dummy"

        cmd = "dummy " + cmd
        args = cmd.split()        
        argsLen = len(args) + 1 # keep the dummy one
        cmd = args[1]
    else:
        argsLen = len(sys.argv)
        args = sys.argv


    if cmd == "disp":                    # display a message
        assert(argsLen>2)
        param = " ".join( args[2:argsLen] ) # join with a space between whatever we got.
        #print( "disp " + param)
        # just assume we want to see the msg
        cad.lcd.backlight_on()
        cad.lcd.clear()
        cad.lcd.write(param)            
    
    elif cmd == "clear":                 # clear the screen and reset cursor pos
        print( "clear")
        cad.lcd.clear()
    
    elif cmd == "blink":                 # blink cursor on or off
        param = args[2].lower()
        print( "blink " + param)
        if param=="on" : 
            cad.lcd.blink_on()
        elif param=="off":
            cad.lcd.blink_off()
        else:
            badParams()
    elif cmd == "press":
        param = args[2].lower()
        print("press " + param)
        if param=="on" : 
            listenForButtonPresses()
        elif param=="off":
            ignoreButtonPresses()
        else:
            badParams()

    elif cmd == "release":
        param = args[2].lower()
        print("release " + param)
        if param=="on" : 
            listenForButtonReleases()
        elif param=="off":
            ignoreButtonReleases()
        else:
            badParams()


    elif cmd == "cursor":                 # show or hide that cursor
        param = args[2].lower()
        print( "cursor " + param)
        if param=="on" : 
            cad.lcd.cursor_on()
        elif param=="off":
            cad.lcd.cursor_off()
        else:
            badParams()
      
    elif cmd == "light":                 # turn the backlight on or off
        param = args[2].lower()
        print( "light " + param)
        if param=="on" : 
            cad.lcd.backlight_on()
        elif param=="off":
            cad.lcd.backlight_off()
        else:
            badParams()

    elif cmd =="move":                  # move left or right
        param = args[2].lower()
        print( "move " + param)
        if param=="left" : 
            cad.lcd.move_left()
        elif param=="right":
            cad.lcd.move_right()
        else:
            badParams()

    elif cmd == "persist":
        if isCalledFromPersist == True :
            print( "blocked persist call" )
        else:    
            print("PIFaceCAD py bridging staying 'resident' ") 
            doPersist()

    elif cmd == "close":
        cad.lcd.backlight_off()
        cad.lcd.clear()
        if isCalledFromPersist==True:
            print("Thankyou and goodnight")
            sys.exit(0)
        else:
            print("close called outside persist mode")
    else:
        # TODO: Something else if we are persistant?
        badParams()


# rough n ready - while loop which will keep us in flight
# pass data via std io.
def doPersist():
    # hmmm thinking readline might be smarter here...

    while True:
        cmd = input()
        # TODO: validate this 
        print("input: " + cmd)
        dispatch(True, cmd)    





#pifaceCAD <cmd>[<param>]

cad = pifacecad.PiFaceCAD() # will cause the display to reinitialise (light off, cursor flashing to 0,0)
pressListener = pifacecad.SwitchEventListener(chip=cad)
pressListenerActive = False
releaseListener = pifacecad.SwitchEventListener(chip=cad)
releaseListenerActive = False


if len(sys.argv) > 1:
    cmd = sys.argv[1].lower()
    
    if len(cmd) > 2:
        dispatch(cmd,cmd)
else:
    badParams()

