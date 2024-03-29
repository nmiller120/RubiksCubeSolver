 /**************************************************************************
 Code for the firmware running on the arduino for the rubiks cube project. The arduino acts as a controller for the assembly, 
 taking commands from the PC. The assembly begins in standby mode where it waits for a command.

  - In "Program" mode the arduino waits for the default positions of each of the servo motors to be loaded into the settingArray
  
  - In "calibration" mode the arduino accepts a continuous stream of commands for the positons of each of the servo motors. Unlike in 
  run mode these positions are a value between 0 and 180 allowing the servo motors to sit anywhere in their full range of motion. 
  This mode is used to determine the setpoints to be downloaded in "Program" mode and used in "run" mode.
  
  - In "run" mode the arduino accepts commands of the form "xYxYxY" where x represents any servo motor from 0 to 7 and Y represents a 
  pre-programmed position. This command can have between 2 and 16 characters.
  
  Example of run commands:
    - 012131 (servos 0, 1, and 3 to position 1)
    - 73 (servo 7 to position 3)
    - 4263 (servo 4 to position 2, servo 6 to position 3)

  The servo motors are divided into 2 groups, linear and radial. Linear moves the claws forward and backward, 
  radial servos rotate the claws. Even rows in the settingArray represent linear, odd rows represent radial. 
  
  Position 0, 1, and 2 for radial servos represent 0, 90 and 180 degrees respectively. 
  Positions 0 and 1 represent 45 and 135 degrees respectively. 
 */
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// constants defined to use in the calculation of the pulse width sent to the servo motor driver
#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

int mode = 0; // 0:standby, 1:program, 2:run
String modeNames[4] = {"standby", "program", "run", "calibration"};
int error_check; // error check to send after programming, program should throw zero, if not there was an error
bool debug = false; // if true, print text to command line
int servoNumber; // servo number, use in run
int servoPos;  // servo position, use in run

char readByte;


int settingArray[8][6]; 
// settingArray: row is servo, col is position, even rows are linear, odd rows are radial
// linear goes 45 pos, 135 pos, 45+ pos, 135+ pos, dummy 90
// radial goes 0 pos, 90 pos, 180 pos, 0+ pos, 90+ pos

void setup(){
  // open serial port, begin communication with the servo driver
  Serial.begin(9600);
  Serial.print(mode);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);  // Analog servos run at ~60 Hz update
}

void loop() {
  // main loop, 4 different modes of operation
  while (Serial.available()==0){}// wait for serial data
  if (mode == 2) {run_mode();} // if in run, run run 
  else if (mode == 3) {calibration();} // if in calibration mode, run calibration
  else if (mode == 0){standby();} //if in standby run standby
  else if(mode == 1){program();} // if in program mode run program 
}

void calibration(){
  /*
     Function reads a semi-continuous stream of data. Each calibration command is coded in ASCII text and is of the form
     1.x.x.x.x.x.x where 1 signals the start of a new command and each x is an integer between 0 and 180. The following code 
     parses those commands and writes them out to the motor controller using the setPWM() function. If a value of -10 is sent 
     to the arduino the assembly returns to standby mode
  */
  while(Serial.available()){
    int readIN = Serial.parseInt();
    if (readIN == 1){
      int servoPos[8];
      for(int i=0; i<8; i++){
        servoPos[i] = Serial.parseInt();
        pwm.setPWM(i, 0, pulseWidth(servoPos[i])); 
        }
      }
    else if (readIN == -10){changeMode(0);}
    }
  }

void run_mode(){
  /*    
    Function reads coded commands from the serial port and moves the motors to match the described positions. Motors 
    That aren't addressed in the command don't move. If the arduino recieves an invalid input the program returns to standby
     
    run mode serial commands: first character refers to the servo to control,
    2nd character refers to the position, ie, "0121" means servo 0 position 1, servo 2
    position 1. The positions are defined during the program phase, which is implemented
    in the code for the __init__() method of this class
  */
  int servoNumber;
  int servoPosition;

  while (Serial.available() < 2) {}
  servoNumber = Serial.read() - '0'; 
  servoPosition = Serial.read() - '0';
  
  if (servoNumber > 7 || servoNumber < 0) {changeMode(0);} // change mode if servo addressed is not in range
  
  if (mode == 2){ // if still in run mode, move servos and change output
    if (debug) {
      Serial.print('\n');
      Serial.print(servoNumber); Serial.print(' '); Serial.print(servoPosition);
      }
    int angle = settingArray[servoNumber][servoPosition];
    pwm.setPWM(servoNumber, 0, pulseWidth(angle));
    }
  }
  
void program(){
  /*
   * This function is how the default position values are loaded to the arduino. The software running on the PC sends the positioning 
   * data as a stream of bytes (ie. 180 is transmitted as a single byte with hex value 0xB4). These values are loaded into the 
   * settingArray. The setting array is a 2d array. Even rows in the array are controlling linear motion, odd rows in the array are 
   * controlling radial motion. 
   *
   * Format of linear = [deg45, deg135, 0, 0, 0, 90] // the 90 degree values act as an error check of the instruction
   * Format of radial = [deg0, deg90, deg180, 0, deg90+, deg180+] deg90+ and deg180+ are slightly more agressive turns to help 
   * allignment of the cube face when turning a side.
   * 
   * Automatically goes back to standby mode after program settings are recieved
   */
  
  while (Serial.available()){
      delay(1000); //give the buffer time to fill
      for (int i=0; i<8; i++){
        for (int j=0; j<6; j++){
          settingArray[i][j] = Serial.read(); // if in program mode load settingArray with data from serial buffer
          }
        }
      
        // error check = 0
        if (settingArray[0][5]==90 && settingArray[2][5]==90 && settingArray[4][5]==90 && settingArray[6][5]==90){error_check = true;} 
   
        if (debug == true){
          Serial.println("Recieved data..."); 
          for (int i=0; i<8; i++){
            for (int j=0; j<6; j++){
              Serial.print(settingArray[i][j]); // if in program mode load setting array with data from serial buffer
              Serial.print(',');               
              }
            Serial.print('\n');
          }
          if (error_check){Serial.println("No Error");} else {Serial.println("Error");}
        }   
        else {
          if (!debug && error_check){Serial.print('y');}
          else {Serial.print('n');}
          }
        changeMode(0);
  }
}

void standby(){
  /*
   * Standby mode waits for a mode change command. Command is a 5 character ascii string. Debug mode can also be toggled in standby. 
   * This just sends debug messsages to the serial port along with the acnowlegments that are sent when debug mode is off. 
   */
  
  char modeSelect[8] = "";
      Serial.readBytes(modeSelect, 5);
      if (!strcmp(modeSelect, "progm")){changeMode(1);} // set to program mode if "program" was recieved in the serial buffer
      else if (!strcmp(modeSelect, "runmd")){changeMode(2);} // set to run if "run" was recieved in the serial buffer
      else if (!strcmp(modeSelect, "check")){checkData();}
      else if (!strcmp(modeSelect, "calib")){changeMode(3);}
      
      else if (!strcmp(modeSelect, "debug")){ // toggle debugging
          if (debug) {
            debug = false;
            changeMode(0);
            } 
           else if (!debug){
              debug = true;
              Serial.print('\n');
              Serial.println("Debugging");
           }
        }  
      else mode = 0;
      while(Serial.available()){Serial.read();}//flush the port
}

void checkData(){
  /*
   * If a check command is recieved in standby mode, this function will write the currently stored settingArray to the serial port
   */
  Serial.println("Recieved data..."); 
  for (int i=0; i<8; i++){
    for (int j=0; j<6; j++){
      Serial.print(settingArray[i][j]); // if in program mode load setting array with data from serial buffer
      Serial.print(',');               
    }
    Serial.print('\n');
  }
  }

void changeMode(int newMode){
  // function invoked when a changemode command is recieved at the serial port
  mode = newMode;
  if (debug == true) {
    Serial.print("In ");
    Serial.print(modeNames[mode]);
    Serial.println(" mode");
    }
  else {Serial.print(mode);}
  }

int pulseWidth(int angle){
  // calculates the pulse width value needed to achieve the desired angle of the servo motor
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return analog_value;
}
