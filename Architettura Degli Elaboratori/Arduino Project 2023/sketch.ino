//DECODE VARIABLES:
volatile byte pulseIndex = 0;
volatile byte signalReceived = 0B00000000;
uint64_t storedSignals = 0; //STORED INFO

//TIMER VARIABLES:
volatile short delaTimeInerrupt;
volatile short previousDeltaTime;
volatile short storedTime;

//PROTOCOL DETECTION VARIABLES:
byte protocolType;
short protocolStartBurstLength[] = {2220, 1110, 840, 590};
//0: NEC, 1:SAMSUNG, 2:JAPAN, 3:SIRCS
bool midwayFlag = false;

int main(){
  outputSetUp();
  timerSetUp();
}

void outputSetUp(){
  DDRD   &= ~(1 << DDD2);    //Pin 2 as input
  PORTD  |= (1 << PORTD2);   //Enable internal pull-up resistor on pin 2
  PCICR  |= (1 << PCIE2);    // Enable Pin Change Interrupt 2
  PCMSK2 |= (1 << PCINT18);  // Enable interrupt for Pin 2
}

void timerSetUp(){
  TCCR1A  = 0; 
  TCCR1B  = 0;
  TCNT1   = 0; 
  TCCR1B |= (1 << CS11) | (1 << CS10); //PRESCALLAR 64:
  OCR1A   = 16875;                     // (67,500 / 4) (16875) old
  TIMSK1 |= (1 << OCIE1A);             // Enable timerinterrupt
  TCCR1B |= (1 << WGM12);
}

ISR(TIMER1_COMPA_vect) {     //Every 67,500 ms
  PCMSK2 |= (1 << PCINT18);  // Enable interrupt for Pin 2 
  pulseIndex = 0;
  midwayFlag = false;
}

ISR(PCINT2_vect) {          //PIN2 interrupt
  if (pulseIndex == 0){timerSetUp();}
  delaTimeInerrupt = TCNT1 - storedTime;
  storedTime = TCNT1;

  if (pulseIndex - 2 <= 0){
    StartOfFrameCheck(delaTimeInerrupt); pulseIndex++; return;
  }
  if ((pulseIndex > 34 && pulseIndex < 51)){
    if (pulseIndex % 2 == 1){previousDeltaTime = delaTimeInerrupt;}
    else {
      if((previousDeltaTime - delaTimeInerrupt > -2)){decode(0);}
      else {decode(1);}
    }
  }
  pulseIndex++;
  if(pulseIndex == 52){
    storeData(); 
    //data collected
  }
}

void decode(byte data) {
  signalReceived >>= 1;           // Shift everything to the left
  signalReceived |= (data << 7);  // Add the new bit
}  

void storeData(){
  for (int i = 0; i < 8; i++) {
    storedSignals = storedSignals << 1;                             // Shift to right
    storedSignals = storedSignals | ((signalReceived >> i) & 0x01); //add bits
  }
}

void StartOfFrameCheck(short time){
  if (pulseIndex == 0){return;}
  if (pulseIndex == 1){
    for (byte i = 0; i < 5; i++){
      if(time - protocolStartBurstLength[i] >= 0){
        midwayFlag = true; protocolType = i;
        return;
      }
    }
  }

  if (pulseIndex == 2 && midwayFlag == true){
    switch (protocolType){
      case 0: if(time - protocolStartBurstLength[1] >= 0){return;} break;
      case 1: if(time - protocolStartBurstLength[1] >= 0){return;} break;
      case 2: if(time - protocolStartBurstLength[2] / 2 >= 0){return;} break;
      case 3: if(time - protocolStartBurstLength[3] / 4 >= 0){return;} break;
    }
  }
  PCMSK2 &= ~(1 << PCINT18);// Disable interrupt for Pin 2
}
