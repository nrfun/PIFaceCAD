#!/usr/bin/python

# PIFaceCAD.py
# Crude wrapper thing so we can call the PIFaceCAD stuff from nodered
# cwhite
# Decemeber 2014

# Import libs - TODO: check pfc is installed!

import sys
import pifacecad

print( 'Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))


    

def badParams():
    print( "Bad parameters - {disp|clear|blink|move|light|in|persist} {str|left|right|on|off|num}")


# process the command we got. Set True if we are persistant... this might help prevent unintentionally recursing
def dispatch(isCalledFromPersist, cmd):
    if cmd == "disp":                    # display a message
        param = sys.argv[2]
        print( "disp " + param)
        # just assume we want to see the msg
        cad.lcd.backlight_on()
        cad.lcd.clear()
        cad.lcd.write(param)            
    
    elif cmd == "clear":                 # clear the screen and reset cursor pos
        print( "clear")
        cad.lcd.clear()
    
    elif cmd == "blink":                 # blink cursor on or off
        param = sys.argv[2].lower()
        print( "blink" + param)
        if param=="on" : 
            cad.lcd.blink_on()
        elif param=="off":
            cad.lcd.blink_off()
        else:
            badParams()



    elif cmd == "cursor":                 # show or hide that cursor
        param = sys.argv[2].lower()
        print( "cursor " + param)
        if param=="on" : 
            cad.lcd.cursor_on()
        elif param=="off":
            cad.lcd.cursor_off()
        else:
            badParams()
      
    elif cmd == "light":                 # turn the backlight on or off
        param = sys.argv[2].lower()
        print( "light " + param)
        if param=="on" : 
            cad.lcd.backlight_on()
        elif param=="off":
            cad.lcd.backlight_off()
        else:
            badParams()

    elif cmd =="move":                  # move left or right
        param = sys.argv[2].lower()
        print( "move " + param)
        if param=="left" : 
            cad.lcd.move_left()
        elif param=="right":
            cad.lcd.move_right()
        else:
            print("test")
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
        dispatch(True, cmd)    





#pifaceCAD <cmd>[<param>]

cad = pifacecad.PiFaceCAD() # will cause the display to reinitialise (light off, cursor flashing to 0,0)

if len(sys.argv) > 1:
    cmd = sys.argv[1].lower()
    
    if len(cmd) > 2:
        dispatch(cmd,cmd)
else:
    badParams()

