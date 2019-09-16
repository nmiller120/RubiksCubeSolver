import serial
import time

class AssemblyController():
    __Serial = None
    __errorCheck = ""
    __delay = 0.5

    def __init__(self):
        # create serial port obj.
        self.__Serial = serial.Serial('COM3',9600, timeout = 1)
        Serial = self.__Serial
        while Serial.in_waiting == 0: # wait for data to arrive at the port
            pass

        print(Serial.read()) # print byte from port

        Serial.write("progm".encode('utf-8')) # set arduino to program mode
        print(Serial.read()) # read response from arduino

        csv_file = "servos.csv"
        aFile = open(csv_file, 'r') # open csv file in read mode

        toSend = ""
        for line in aFile:
            line = line.strip()
            csv_line = line.split(",")
            for x in range(6):
                toSend += chr(int(csv_line[x])) # read csv values into 'toSend'

        ##print(" ".join(str(ord(c)) for c in toSend)) # returns 'toSend' in dec
        Serial.write(toSend) # write 'toSend' data to arduino

        while (Serial.in_waiting==0): # wait for response
            pass

        while (Serial.in_waiting): # read response
            print(Serial.read()) # print response

        Serial.write("runmd".encode("utf-8"))
        print(Serial.read())

    def rightCCW(self):
        #rotate right CCW
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
        #rotate right CW
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
        #rotate front CCW
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
        #rotate front CCW
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
        instruction = '0110213041506170'
        self.__Serial.write(instruction)

    def all_engaged(self):
        instruction = '0010203040506070'
        self.__Serial.write(instruction)

    def kociemba(self, kociemba_string):
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
        # face selection is F, R, B, L
        # maps to ( 1 + 2*n ) : n = 0, 1, 2, 3
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

    def show_face(self, new_top, new_front):
        
        if new_front == self.cube.back:
            self.cube.rotate("right", "CCW")

        if new_front == self.cube.bottom:
            self.cube.rotate("right", "CCW")
            self.cube.rotate("right", "CCW")

        if new_front == self.cube.front:
            self.cube.rotate("right", "CW")

        if new_front == self.cube.right:
            self.cube.rotate("front", "CCW")

        if new_front == self.cube.left:
            self.cube.rotate("front", "CW")

        self.cube.rotate("right", "CCW")

        if new_top == self.cube.top:
            print "Done."

        if new_top == self.cube.left:
            self.cube.rotate("front", "CW")
            print "Done."

        if new_top == self.cube.right:
            self.cube.rotate("front", "CCW")
            print "Done."

        if new_top == self.cube.bottom:
            self.cube.rotate("front", "CCW")
            self.cube.rotate("front", "CCW")
            print "Done."

class Orientation():
    """Class needs updated, supposed to be an object to track the orientation 
    of the rubiks cube"""
    up = None
    front = None
    right = None
    down = None
    back = None
    left = None

    __layout = ["W", "Y", "R", "O", "B", "G"]
    __tfr_layout = ["W", "R", "B"]

    def __init__(self, upChr, frontChr):
        self.reorient(upChr, frontChr)

    def rotate(self, about_axis, rotate):
        """about_axis = 'front' or 'right' 
           rotate = 'CW' or 'CCW'"""
        print "About " + about_axis + " rotate " + rotate
        if about_axis == "right":
            faces = [self.up, self.back, self.down, self.front]
            if rotate == "CCW":
                self.up = faces[1]
                self.back = faces[2]
                self.down = faces[3]
                self.front = faces[0]

            if rotate == "CW":
                self.up = faces[3]
                self.back = faces[0]
                self.down = faces[1]
                self.front = faces[2]

        if about_axis == "front":
            faces = [self.top, self.right, self.bottom, self.left]
            if rotate == "CCW":
                self.top = faces[1]
                self.right = faces[2]
                self.bottom = faces[3]
                self.left = faces[0]

            if rotate == "CW":
                self.up = faces[3]
                self.right = faces[0]
                self.down = faces[1]
                self.left = faces[2]

    def reorient(self, newUp, newFront):
        self.up = newUp
        self.front = newFront
        up_sign = None
        front_sign = None
        up_direction = None
        front_direction = None
        right_direction = None
        right_sign = None

        for x in range(6):
            if self.__layout[x] == newUp and x % 2==0:
                self.down = self.__layout[x+1]
                up_sign = 1
                up_direction = x//2

            if self.__layout[x] == newUp and x % 2==1:
                self.down = self.__layout[x-1]
                up_sign = -1
                up_direction = x//2

            if self.__layout[x] == newFront and x % 2==0:
                self.back = self.__layout[x+1]
                front_sign = 1
                front_direction = x//2

            if self.__layout[x] == newFront and x % 2==1:
                self.back = self.__layout[x-1]
                front_sign = -1
                front_direction = x//2

        loop = [0, 1, 2, 0, 1, 2]

        for x in range(6):
            if up_direction == loop[x]:
                if front_direction == loop[x+1]:
                    right_direction = loop[x+2]
                    right_sign = 1

                else:
                    y = 5 - x
                    loop.reverse()
                    right_direction = loop[(y+2)%6]
                    right_sign = -1

                break

        if up_sign * front_sign * right_sign > 0:
            self.right = self.__layout[right_direction*2]
            self.left = self.__layout[right_direction*2 + 1]

        else:
            self.right = self.__layout[right_direction*2 + 1]
            self.left = self.__layout[right_direction*2]
