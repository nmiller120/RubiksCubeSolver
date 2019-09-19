# Automated Rubiks Cube Solver

Ongoing work-in-progress. Goal is to design a system that is able to grab and automatically solve a Rubik's Cube after reading the colors off of the cube via a webcam. A demonstration of the mechanical portion of the build can be seen via the following youtube link: https://www.youtube.com/watch?v=32NWT3KxtNk. A demonstration of the color calibration utility can be seen here: https://www.youtube.com/watch?v=5z36a5fC41Q

## Mechanical Design

Parts were designed in Autodesk Inventor, the cross sections of the parts were copied into Autocad and laid out on a single sheet. The file was exported again this time as a .dxf file. This file was then sent to Ponoko to be lasercut.

The actuators are all standard size hobby servo motors, primarily used in RC cars. They are cheap, fairly powerful, and easy to control.

## Electrical Design

The Arduino acts as the controller for the servo motor assembly. It interfaces with a servo motor driver board to control the 8 servos. The arduino recieves serial commands from the program running on my laptop via USB. These commands are decoded into smaller instructions that are passed down to ther servo driver.

## Software Design

The goal of the project is to have the program start by moving the assembly, showing the layout of the cube to a webcam mounted above. A computer vision algorithm is to be applied to the video feed, detecting the colors on the cube's faces and recording that data into memory. Once all of the faces have been read, the data recorded is to be passed to the Kociemba algorithm. The algorithm outputs instructions on how the cube is to be solved. The AssemblyController module then parses those instructions and determines how each of the given instructions is to be implemented and relays that information to the arduino by commanding the positioning of the assembly's servo motors. A demo of the mechanical assembly working a solution can be seen above, as well as a demo on how the HSV filtering values are calibrated.

I have spent a lot of time commenting and adding documentation to the code for this project. I am trying to keep the code in as readable of condition as possible. Feel free to read through the project files as they may shed light on some of the more of the technical details of the project not covered here. 

Thanks for reading!

### Additional Links:
Kociemba Algorithm: https://github.com/muodov/kociemba  
Open CV Library: https://pypi.org/project/opencv-python/
