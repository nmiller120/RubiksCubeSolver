from __future__ import print_function
import Objects_GUI as gui
import Objects_File as files
import Objects_Color as color
import Objects_Overlay as overlay
import Objects_FaceletDetection as detection
import Objects_CubeControl as cubes

from Tkinter import *
import numpy as np
import cv2
import serial
import time
import kociemba
from string import maketrans

def mechanicalDemo1(cubeStr, waitTime):
    """To solve the cube with a hardcoded cube map, cubeStr is the cube map
    and waitTime is the time to delay before the assembly grabs the cube"""

    cubeStr = convertInput(cubeStr, "URF") # convert from pos to color
    solution = kociemba.solve(cubeStr) # get solution string
    control = cubes.AssemblyController() # create a control object
    control.all_retract() # retract all arms
    time.sleep(waitTime) # wait for the cube to get into position
    control.all_engaged() # engage claws
    control.kociemba(solution) # exicute instruction string
    time.sleep(0.5) # wait
    control.all_retract() # release cube

def convertInput(kociembaIN, toWhat):
    """Change the input string to and from color. toWhat is either
    'URF' or 'WBR'"""
    replace = 'WBRYGO'
    replace_with = 'URFDLB'

    if toWhat is 'URF':
        replace = 'WBRYGO'
        replace_with = 'URFDLB'

    elif toWhat is 'WBR':
        replace = 'URFDLB'
        replace_with = 'WBRYGO'

    transtab = maketrans(replace,replace_with)
    print(kociembaIN)
    return kociembaIN.translate(transtab)

def servoCalibration():
    """Runs the servo setup gui, only for testing the default position
    of the servo motors"""
    ser = serial.Serial('COM3',9600)
    time.sleep(2);
    #ser.write("debug".encode("utf-8"))
    ser.write("calib".encode("utf-8"))
    time.sleep(1);

    root = Tk()
    root.title("Main Window")
    root.geometry('600x700')
    setup_app = gui.Setup_Servo_Window(root)

    for x in range(4):
        y = x*2
        setup_app.scale_widgets[y].set(50)

    while True:
        try:
            setup_app.update_idletasks()
            setup_app.update()
            serial_str = "1."

            for x in range(8):
                text = str(setup_app.scale_widgets[x].get())
                serial_str += text + "."

            serial_str += "\n"
            ser.write(serial_str)

        except:
            while (ser.in_waiting):
                print(ser.read(), end='')
            break

def colorCalibration(cap = None):
    """Color Calibration gui, to set the minumum and maximum hsv values
     cap: capture object"""

    #create "root" for Main Window
    root = Tk()
    root.title("Main Window")
    root.geometry('600x700')

    frame = None
    if cap == None:
        frame = cv2.imread("rcube.jpg")

    else:
        ret, frame = cap.read()

    #cv2.imshow("Frame", frame)

    mask = overlay.Mask()

    # Create Main Window
    setup_app = gui.Setup_Color_Window(root)

    #begin loop, end when setup is complete
    while not setup_app.is_complete():
        try:
            #pull image from feed
            if cap != None:
                ret, frame = cap.read()

            #add mask overlay to image
            img = mask.parse_cap(frame, setup_app.get_lower_range(), setup_app.get_upper_range(), setup_app.is_exclusive())

            #update setup app
            setup_app.update_idletasks()
            setup_app.update()

            #display image
            cv2.imshow("Frame", img)

        except TclError:
            cap.release()
            cv2.destroyAllWindows()
            break


    #if "finished" is pressed close windows
    if setup_app.is_complete():

        root.destroy()
##        cap.release()
        cv2.destroyAllWindows()

def main():
    mechanicalDemo1("WYOYWRGBBRGBOBGWYWROWORYROOBGGWYBYWGORYBGWGBYYGBWORRRO",4.0)

if __name__ == '__main__':
    main()


##References:
##      http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
##      Tutorial 5
