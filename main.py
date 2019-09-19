# Rubik's Cube Solver Project
# Nick Miller
# Last Update: Feb, 2018

import RubiksGUIs as gui # contains classes used for the calibration gui
import AssemblyController as cubes # implements the lower level control of the
# rubiks cube, moves the servo assembly
import Mask as overlay #
from tkinter import * # library for implementing guis
import cv2 # library for implementing computer vision, has algorithms for color
# image processesing and api for reading data from webcams and image files
import serial # library for implementing the serial interface with the arduino
import time # used primarily in this project to implement wait functions
import kociemba # Implements the kociemba algorithm, given a cube map it provides
# a function that will return a string representing the instructions to solve the
# rubiks cube.

def mechanicalDemo(cubeStr, waitTime):
    # Method used to solve the cube with a hardcoded cube map, cubeStr is the
    # cube map, waitTime is the time to delay before the assembly grabs the cube

    cubeStr = convertInput(cubeStr, "URF") # convert from position reference to color reference
    solution = kociemba.solve(cubeStr) # get solution string from kociemba algorithm
    control = cubes.AssemblyController() # create a control object
    control.all_retract() # retract all arms
    time.sleep(waitTime) # wait some time for the cube to get into position
    control.all_engaged() # engage claws
    control.kociemba(solution) # execute instruction string
    time.sleep(0.5) # wait
    control.all_retract() # release cube

def convertInput(kociembaIN, toWhat):
    # the kociemba algorithm accepts a general cube map string that is agnostic to
    # what color the faces are. In this formatting the sides are labeled as 'u', 'r'
    # 'f', 'd', 'l' and, 'b' for up, right, down, front, down, left, and back. This
    # method is used to convert between kociemba's general cube mapping and a cube
    # mapping based on the colors of the faces.

    # The functions argument kociembaIN is a general cube map string,
    # toWhat is a string representing what the desired reference, color or orientation.
    # Color is denoted by passing thestring "URF" and orientation is denoted by
    # passing the string "WBR"

    replace = 'WBRYGO'
    replace_with = 'URFDLB'

    if toWhat is 'URF':
        replace = 'WBRYGO'
        replace_with = 'URFDLB'

    elif toWhat is 'WBR':
        replace = 'URFDLB'
        replace_with = 'WBRYGO'

    transtab = {ord(x): y for (x, y) in zip(replace, replace_with)}
    print(kociembaIN)
    return kociembaIN.translate(transtab)

def servoCalibration():
    # This function implements positioning calibration for the project.
    # The intended use is to move the servomotors using the sliders on the GUI
    # when a desired position for the position of the servomotor is found, write
    # down the value and what position number it corresponds to. After proper positioning
    # of each servomotor is found the default settings are to be recorded in the
    # file servos.csv which then provides configuration parameters for the project when
    # sending commands to the servo assembly in "run" mode.

    ser = serial.Serial('COM3',9600)
    time.sleep(2);
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

def colorCalibration(capSource = None):
    # Color Calibration gui, this function implements a system for calibrating
    # the color filter settings for the computer vision portion of the project.
    # Sliders allow the user to set the min and max HSV values for the filter for
    # each of the 6 cube face colors as well as filters to remove background colors
    #
    # The argument capSource is an integer represeting the disired video capture source,
    # If there are multiple webcams connected to your pc you select them with the
    # integer. The default value of None opens an image file "rcube.jpeg".

    root = Tk()
    root.title("Main Window")
    root.geometry('600x700')

    frame = None
    if capSource == None:
        frame = cv2.imread("rcube.jpg")

    else:

        cap = cv2.VideoCapture(capSource)
        ret, frame = cap.read()

    mask = overlay.Mask()

    # Create Main Window
    setup_app = gui.Setup_Color_Window(root)

    # begin loop, end when setup is complete
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
        cv2.destroyAllWindows()

def main():
    # servoCalibration()
    # mechanicalDemo("WYOYWRGBBRGBOBGWYWROWORYROOBGGWYBYWGORYBGWGBYYGBWORRRO",4.0)
    colorCalibration(0)

if __name__ == '__main__':
    main()


##References:
##      http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
##      Tutorial 5
