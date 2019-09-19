# Module defines a single class AssemblyController which handles all communication
# with the servo assembly.

# When solving the cube, first the controller object is created, then the kociemba
# SOLUTION string is passed to the class method kociemba(). This method parses
# the solution string and sends the arduino controlling the assembly a series of
# instruction codes describing the positions of the servo motors needed to solve
# the puzzle. The class methods are all public and can be called as needed.

# serial commands: first character refers to the servo to control, 2nd character refers
# to the position, ie, "0121" means servo 0 position 1, servo 2 position 1. The positions
# are defined during the program phase in the code for the  __init__() function of this
# class

import serial
import time

class AssemblyController():

    __Serial = None
    __delay = 0.5 # time the system waits for the servomotors to get into position

    def __init__(self):

        # create serial port obj.
        self.__Serial = serial.Serial('COM3',9600, timeout = 1)
        Serial = self.__Serial
        while Serial.in_waiting == 0: # wait for data to arrive at the port
            pass

        print(Serial.read()) # print byte from port

        Serial.write("progm".encode('utf-8')) # set arduino to program mode
        print(Serial.read()) # read response from arduino

         # load servo default position values from csv file
        csv_file = "servos.csv"
        aFile = open(csv_file, 'r') # open csv file in read mode

        toSend = ""
        for line in aFile:
            line = line.strip()
            csv_line = line.split(",")
            for x in range(6):
                toSend += chr(int(csv_line[x])) # read csv values into 'toSend'

        Serial.write(toSend) # write 'toSend' data to arduino

        while (Serial.in_waiting==0): # wait for response
            pass

        while (Serial.in_waiting): # read response
            print(Serial.read()) # print response

        Serial.write("runmd".encode("utf-8"))
        print(Serial.read())

    def rightCCW(self):
        # method rotates the entire cube about the right axis CCW
        delay = self.__delay
        Serial = self.__Serial
        self.all_engaged()
        time.sleep(delay)
        Serial.write('2161') #1
        time.sleep(delay)
        Serial.write('7131') #2
        time.sleep(delay)
        Serial.write('2060') #3
        time.sleep(delay)
        Serial.write('0141') #4
        time.sleep(delay)
        Serial.write('3072') #5
        time.sleep(delay)
        Serial.write('0040') #6
        time.sleep(delay)
        Serial.write('61') #7
        time.sleep(delay)
        Serial.write('70') #8
        time.sleep(delay*1.5)
        Serial.write('60') #9
        time.sleep(delay)

    def rightCW(self):
        # method rotates the entire cube about the right axis clockwise
        delay = self.__delay
        Serial = self.__Serial
        self.all_engaged()
        time.sleep(delay)
        Serial.write('2161') #1
        time.sleep(delay)
        Serial.write('7131') #2
        time.sleep(delay)
        Serial.write('2060') #3
        time.sleep(delay)
        Serial.write('0141') #4
        time.sleep(delay)
        Serial.write('3270') #5
        time.sleep(delay)
        Serial.write('0040') #6
        time.sleep(delay)
        Serial.write('21') #7
        time.sleep(delay)
        Serial.write('30') #8
        time.sleep(delay*1.5)
        Serial.write('20') #9
        time.sleep(delay)

    def frontCCW(self):
        # method rotates the entire cube about the front axis counter-clockwise
        delay = self.__delay
        Serial = self.__Serial
        self.all_engaged()
        time.sleep(delay)
        Serial.write('0141') #1
        time.sleep(delay)
        Serial.write('1151') #2
        time.sleep(delay)
        Serial.write('0040') #3
        time.sleep(delay)
        Serial.write('6121') #4
        time.sleep(delay)
        Serial.write('1052') #5
        time.sleep(delay)
        Serial.write('2060') #6
        time.sleep(delay)
        Serial.write('41') #7
        time.sleep(delay)
        Serial.write('50') #8
        time.sleep(delay*1.5)
        Serial.write('40') #9
        time.sleep(delay)

    def frontCW(self):
        # method rotates the entire cube about the front axis clockwise
        delay = self.__delay
        Serial = self.__Serial
        self.all_engaged()
        time.sleep(delay)
        Serial.write('0141') #1
        time.sleep(delay)
        Serial.write('1151') #2
        time.sleep(delay)
        Serial.write('0040') #3
        time.sleep(delay)
        Serial.write('6121') #4
        time.sleep(delay)
        Serial.write('1250') #5
        time.sleep(delay)
        Serial.write('2060') #6
        time.sleep(delay)
        Serial.write('01') #7
        time.sleep(delay)
        Serial.write('10') #8
        time.sleep(delay*1.5)
        Serial.write('00') #9
        time.sleep(delay)

    def all_retract(self):
        # method retracts all claws
        instruction = '0110213041506170'
        self.__Serial.write(instruction)

    def all_engaged(self):
        # method extends all claws
        instruction = '0010203040506070'
        self.__Serial.write(instruction)

    def kociemba(self, kociemba_string):
        # method implements the kociemba solution
        # Example of kociemba string:
        # "R' D2 R' U2 R F2 D B2 U' R F' U R2 D L2 D' B2 R2 B2 U' B2"

        sides = ['F', 'R', 'B', 'L', 'U', 'D']
        inst = kociemba_string.split(' ')
        size = len(inst)
        print(size)

        for x in range(size):
            rotation = None
            if len(inst[x]) == 1:
                rotation = "CW"

            elif inst[x][1] == '\'':
                rotation = "CCW"

            elif inst[x][1] == '2':
                rotation = "2CW"

            for y in range(4):
                if inst[x][0] == sides[y]:
                    self.turn_face(y, rotation)

            if inst[x][0] == 'U':
                self.rightCCW()
                self.turn_face(0, rotation)
                self.rightCW()

            if inst[x][0] == 'D':
                self.rightCW()
                self.turn_face(0, rotation)
                self.rightCCW()

    def turn_face(self, face_selection, rotate):
        # method turns the selected face by the given amount, either clockwise 90 deg,
        # counter clockwise 90 deg, or clockwise 180 deg.

        # face selection is F, R, B, L
        # maps to ( 1 + 2*n ) : n = 0, 1, 2, 3

        # rotate is a string of the follwing values "CW", "CCW", or "2CW"

        Serial = self.__Serial
        delay = self.__delay * 2
        self.all_engaged()

        L = str(2*face_selection)
        R = str(2*face_selection+1)

        if rotate == 'CW':
            Serial.write(R+'4')
            time.sleep(delay)
            Serial.write(L+'1')
            time.sleep(delay)
            Serial.write(R+'0')
            time.sleep(delay)
            Serial.write(L+'0')
            time.sleep(delay)

        if rotate == '2CW':
            Serial.write(R+'5')
            time.sleep(delay)
            Serial.write(L+'1')
            time.sleep(delay)
            Serial.write(R+'0')
            time.sleep(delay)
            Serial.write(L+'0')
            time.sleep(delay)

        if rotate == 'CCW':
            Serial.write(L+'1')
            time.sleep(delay)
            Serial.write(R+'1')
            time.sleep(delay)
            Serial.write(L+'0')
            time.sleep(delay)
            Serial.write(R+'3')
            time.sleep(delay)