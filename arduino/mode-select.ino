const int RU = 2;
const int RD = 3;
int mode = 2;
void modechange(int);
void setup() {
  pinMode(RU, INPUT_PULLUP);
  pinMode(RD, INPUT_PULLUP);
  for(int i=6;i<12;i++){
    pinMode(i, OUTPUT);
    digitalWrite(i,HIGH);
    }
    pinMode(12, OUTPUT);
    digitalWrite(12,LOW);
}

void loop() {
  int buttonState1 = digitalRead(RU);
  int buttonState2 = digitalRead(RD);
  if ((mode<5) && (buttonState1 == LOW)) {
    while(buttonState1 == LOW)
    {
      delay(50);
      buttonState1 = digitalRead(RU);
    }
    
    mode++;
    modechange(mode);
    }
   else if ((mode>1) && (buttonState2 == LOW)){
    while(buttonState2 == LOW)
    {
      delay(50);
      buttonState2 = digitalRead(RD);
    }
    mode--;
    modechange(mode);
  }
}
void modechange(int m)
{
  if (mode == 2)
  {
    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, LOW);
    
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
  }
  else if (mode == 3)
  {
    digitalWrite(10, HIGH);
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    
    digitalWrite(6, LOW);
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
  }
  else if (mode == 4)
  {
    digitalWrite(10, HIGH);
    digitalWrite(11, LOW);
    digitalWrite(12, HIGH);
    
    digitalWrite(6, HIGH);
    digitalWrite(7, LOW);
    digitalWrite(8, HIGH);
    digitalWrite(9, HIGH);
  }
  else if (mode == 5)
  {
    digitalWrite(10, LOW);
    digitalWrite(11, LOW);
    digitalWrite(12, HIGH);
    
    digitalWrite(6, HIGH);
    digitalWrite(7, LOW);
    digitalWrite(8, LOW);
    digitalWrite(9, HIGH);
  }
  else if (mode == 1)
  {

    digitalWrite(10, HIGH);
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    
    digitalWrite(6, HIGH);
    digitalWrite(7, HIGH);
    digitalWrite(8, HIGH);
    digitalWrite(9, LOW);
  }
}
