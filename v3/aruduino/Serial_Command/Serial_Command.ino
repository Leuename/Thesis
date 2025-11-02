void serialEvent(){
  String serial = Serial.readStringUntil('\n');
  Serial.println(serial);

  if(false){}
  else if(serial == "mlcw"){ left motor up
    digitalWrite(dirPinL,1); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinL,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinL,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mlcc"){ motor left below
    digitalWrite(dirPinL,0); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinL,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinL,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mrcw"){  right motor up 
    digitalWrite(dirPinR,1); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinR,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinR,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mrcc"){ right motor below 
    digitalWrite(dirPinR,0); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinR,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinR,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mccw"){ reverse
    digitalWrite(dirPinC,1); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinC,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinC,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mccc"){ forward
    digitalWrite(dirPinC,0); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 800; x++) {
      digitalWrite(stepPinC,1); 
      delayMicroseconds(700);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinC,0); 
      delayMicroseconds(700); 
    }
  }
  else if(serial == "mpcw"){ forward push 
    digitalWrite(dirPinP,1); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 400; x++) {
      digitalWrite(stepPinP,1); 
      delayMicroseconds(1000);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinP,0); 
      delayMicroseconds(1000); 
    }
  }
  else if(serial == "mpcc"){ reverse of push
    digitalWrite(dirPinP,0); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x < 400; x++) {
      digitalWrite(stepPinP,1); 
      delayMicroseconds(1000);    // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPinP,0); 
      delayMicroseconds(1000); 
    }
  }
  else if(serial == "lmits"){
    while(true){
      String command = Serial.readStringUntil('\n');
      Serial.println(command);
      if(command == "stop"){
        break;
      }
      Serial.print("limitL: ");
      Serial.println(digitalRead(lsL));
      Serial.print("limitR: ");
      Serial.println(digitalRead(lsR));
      Serial.print("limitP: ");
      Serial.println(digitalRead(lsP));
    }
  }
  else if (serial == "phome") { 
    Home(stepPinP,dirPinP,lsP,1);
  }
  else if (serial == "lhome") {
    Home(stepPinL,dirPinL,lsL);
  }
  else if (serial == "rhome") {
    Home(stepPinR,dirPinR,lsR);
  }
}