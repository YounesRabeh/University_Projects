volatile bool isSignalFinished = false;
volatile bool isSignalStarted = false;
volatile bool isFirstInterrupt = true;


byte byteIndex = 0;
volatile byte signalReceived = 0B00000000;


#define NEC_START_FRAME_HIGH_TIME 2249 //9000
#define NEC_START_FRAME_LOW_TIME 1125 //4000
#define NEC_ZERO_TIME_INTERVAL 263 //1250
#define NEC_ONE_TIME_INTERVAL 553 //2250
#define NEC_COMMAND_SIGNAL_STARTING 10125// 40500

byte pulseIndex = 0;
volatile short decodedTimeSignal;



void setup() {
  Serial.begin(9600);
  outputSetUp();
  timerSetUp();
}


void loop() {
  
}

ISR(TIMER1_COMPA_vect) {
  //Every 67,500 ms
  isFirstInterrupt = true;
  pulseIndex = 0;
  byteIndex = 0;
}

void timerSetUp(){
  TCCR1A = 0; 
  TCCR1B = 0;
  TCNT1 = 0; 
  TCCR1B |= (1 << CS11) | (1 << CS10);//PRESCALLAR 64:
  OCR1A = 16875; // (67,500 / 4)
  TIMSK1 |= (1 << OCIE1A);// Enable timerinterrupt
  TCCR1B |= (1 << WGM12);
}

void outputSetUp(){
  DDRD &= ~(1 << DDD2);   //Pin 2 as input
  PORTD |= (1 << PORTD2); //Enable internal pull-up resistor on pin 2

  PCICR |= (1 << PCIE2); // Enable Pin Change Interrupt 2
  PCMSK2 |= (1 << PCINT18); // Enable interrupt for Pin 2 (PCINT18)
}

volatile int _time;
volatile unsigned int timeWhenInterrupted = 0;

volatile bool isThisStartFrame = false;

volatile int ___time = 0;
volatile int storedTime = 0;
volatile bool isValidSample = false; 

ISR(PCINT2_vect) {
  timeWhenInterrupted = TCNT1;
  if(pulseIndex < 3){
    startFrameCheck();
  }
  if(pulseIndex == 2 && isThisStartFrame){
    isSignalStarted = true;

  }else if(isSignalStarted && (pulseIndex >= 34 && pulseIndex <= 51)){
    short timeDifference = timeWhenInterrupted - storedTime;
    if(byteIndex < 8){
      if(timeDifference - NEC_ONE_TIME_INTERVAL >= 0){
        decode(1);
        byteIndex++;
      }else if (timeDifference - NEC_ZERO_TIME_INTERVAL >= 0){
        decode(0);
        byteIndex++;
      }
    }
    isValidSample = !isValidSample; 
    if(isValidSample){
      storedTime = timeWhenInterrupted;
    }
  }
  
  pulseIndex++;
  if(isSignalStarted && pulseIndex == 52){
    buttons();
  }
}

void decode(byte value){
  byte index = byteIndex;
  byte mask = 1 << index;
  signalReceived &= ~mask;
  if (value == 1) {
    signalReceived |= mask;
  }
}

void startFrameCheck(){
  if (isFirstInterrupt) {
    isFirstInterrupt = false;
    timerSetUp();
    return;
  } 
  //Serial.println(timeWhenInterrupted);
  if(timeWhenInterrupted == NEC_START_FRAME_HIGH_TIME){
    _time = timeWhenInterrupted;
    return;
  }
  if((timeWhenInterrupted - _time) == NEC_START_FRAME_LOW_TIME){
    isThisStartFrame = true;
  }else{
    isThisStartFrame = false;
  }

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

