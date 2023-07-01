void setup() {
  Serial.begin(115200);
  outputSetUp();
  timerSetUp();
}

volatile byte pulseIndex = 0;
volatile byte signalReceived = 0B00000000;


void loop() {
  // put your main code here, to run repeatedly:

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
}

volatile short delaTimeInerrupt;
volatile short previousDeltaTime;
volatile int storedTime;

ISR(PCINT2_vect) {          //PIN2 interrupt
  if (pulseIndex == 0){timerSetUp();}
  delaTimeInerrupt = TCNT1 - storedTime;
  storedTime = TCNT1;

  if (pulseIndex - 2 <= 0){
    isStartOfFrame(delaTimeInerrupt); pulseIndex++; return;
  }
  if ((pulseIndex > 34 && pulseIndex < 51)){
    if (pulseIndex % 2 == 1){previousDeltaTime = delaTimeInerrupt;}
    else {
      if((delaTimeInerrupt - 415 > 0)){decode(1);} //(previousDeltaTime - 135 < 0) for the 0
      else {decode(0);}
    }
  }
  pulseIndex++;
  if(pulseIndex == 52){
    buttons();
  }
}

void decode(byte bit) {
  signalReceived >>= 1;          // Shift everything to the left
  signalReceived |= (bit << 7);  // Add the new bit
}  

bool midwayFlag = false;
void isStartOfFrame(short time){
  
  if (pulseIndex == 0){return;}
  if (pulseIndex == 1 && time >= 2200){midwayFlag = true;return;}
  if (pulseIndex == 2 && midwayFlag == true && time <= 1225){return;}

  else {PCMSK2 &= ~(1 << PCINT18);}// Disable interrupt for Pin 2
}

void buttons(){
  Serial.print("You pressed: ");
  switch (signalReceived) {
    case 162:
      Serial.println("POWER");
      break;
    case 226:
      Serial.println("MENU");
      break;
    case 34:
      Serial.println("TEST");
      break;
    case 2:
      Serial.println("PLUS");
      break;
    case 194:
      Serial.println("BACK");
      break;
    case 224:
      Serial.println("PREV.");
      break;
    case 168:
      Serial.println("PLAY");
      break;
    case 144:
      Serial.println("NEXT");
      break;
    case 104:
      Serial.println("0");
      break;
    case 152:
      Serial.println("MINUS");
      break;
    case 176:
      Serial.println("C");
      break;
    case 48:
      Serial.println("1");
      break;
    case 24:
      Serial.println("2");
      break;
    case 122:
      Serial.println("3");
      break;
    case 16:
      Serial.println("4");
      break;
    case 56:
      Serial.println("5");
      break;
    case 90:
      Serial.println("6");
      break;
    case 66:
      Serial.println("7");
      break;
    case 74:
      Serial.println("8");
      break;
    case 82:
      Serial.println("9");
      break;
    default:
      Serial.print("UNKNOWN::SignalCode[byte]: ");
      Serial.println(signalReceived);     
  }
}



