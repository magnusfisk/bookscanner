/* Script for running the pageturn mechanism
Sets the pageturntime remotely over serial port
This feature has not worked before...
Created by Magnus Axelson-Fisk
*/

#include <Servo.h>

Servo pageTurnServo;
Servo pageHoldServo;
int servoPosTurn = 0;
int servoPosHold = 0;



int pageTurnTime = 0;
int pageHoldTime = 600;

String inputVar = "";
boolean variableSet = false;
boolean startSignal = false;
boolean Hold = false;

void setup() {
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  pageTurnServo.attach(9);
  pageHoldServo.attach(8);
  
  Serial.begin(9600);
  inputVar.reserve(10);

  
}

boolean resetFunction() {
  
  pageTurnTime = 0;
  pageHoldTime = 0;
  startSignal = 0;
  variableSet = false;
  inputVar = "";
  return true;
  
}

void pageHold (boolean Hold) { //If Hold=1 the scanner will hold left pages, if 0 the scanner will open up to add swipe more pages
  if (Hold) {
    servoPosHold = 85;
    pageHoldServo.write(servoPosHold);
  
  }
  else {
    servoPosHold = 0;
    pageHoldServo.write(servoPosHold);
  }
}


void loop() {
  pageTurnServo.write(180);
  
  if (startSignal) { //if there has been a signal from RPi the program executes this code
    digitalWrite(7, LOW);
    digitalWrite(5, HIGH); //spin clockwise, seen in front
    digitalWrite(6, LOW);
    delay(pageTurnTime);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);

    for (servoPosTurn = 180; servoPosTurn>= 1; servoPosTurn -= 1) { //Swipes arm so that page folds over
      pageTurnServo.write(servoPosTurn);
      delay(5);
      if (servoPosTurn == 80) { //Releases pages so that new pages can be turned
      Hold = false;
      pageHold(Hold);
      }
        
    }
    
    Hold = true;        //Makes sure the left pages are held
    pageHold(Hold);   
    delay(50);
    
    digitalWrite(4, HIGH); //Tightens left page
    delay(pageHoldTime);
    digitalWrite(4, LOW);

    
    pageTurnServo.write(0); //turns back the swipearm

    delay(20);

    digitalWrite(5, LOW);    //tightens right page
    digitalWrite(6, HIGH);
    delay(pageHoldTime);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    Serial.println(startSignal);

    startSignal = false;
}
    
}

void serialEvent() {
boolean resetComplete = false;
  inputVar = Serial.readString();
  int switchVar =  inputVar.toInt();

  switch (switchVar) {
   case 1:
    startSignal = true;
    inputVar = "";
    break;
   case 9:
    resetComplete = resetFunction();
    Serial.println(resetComplete); //returns 1 if successful or 0 if unsuccessful to RPi
    inputVar=""; 
    break;
   default:
    if (variableSet==false) {
        pageTurnTime = inputVar.toInt();
        variableSet = true;
        Serial.println(variableSet);
        inputVar=""; 
    }
    break;
  }
}



