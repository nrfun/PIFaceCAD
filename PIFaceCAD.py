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

#pifaceCAD <cmd>[<param>]

cad = pifacecad.PiFaceCAD()

if len(sys.argv) > 1:
    cmd = sys.argv[1].lower()
    

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
            badParams()

   
else:
    badParams()



def badParams():
    print( "Bad parameters - {disp|clear|blink|move|light} {str|left|right|on|off}")
