#define stepPinL 4
#define dirPinL 5 
#define stepPinR 6
#define dirPinR 7 
#define stepPinC 8
#define dirPinC 9 
#define stepPinP 2
#define dirPinP 3

#define lsL 24
#define lsR 26
#define lsP 22

void setup() {
  // Sets the two pins as Outputs
  Serial.begin(9600);
  pinMode(stepPinL,OUTPUT); 
  pinMode(stepPinR,OUTPUT);
  pinMode(stepPinC,OUTPUT);
  pinMode(stepPinP,OUTPUT); 
  pinMode(dirPinL,OUTPUT); 
  pinMode(dirPinR,OUTPUT); 
  pinMode(dirPinC,OUTPUT);
  pinMode(dirPinP,OUTPUT);

  pinMode(lsL, INPUT_PULLUP);
  pinMode(lsR, INPUT_PULLUP);
  pinMode(lsP, INPUT_PULLUP);
}
void loop() {
}

void Home(uint8_t pulse,uint8_t dir, uint8_t ls,int dec=0){
  delay(50);
  digitalWrite(dir, dec);
  while(digitalRead(ls)==1){
    Serial.println(digitalRead(ls));
    digitalWrite(pulse,1); 
    delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
    digitalWrite(pulse,0); 
    delayMicroseconds(700); 
  }
  digitalWrite(pulse,1);
  delay(200);
  Serial.println("STOP");
}