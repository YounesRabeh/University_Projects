


//________________________________________________________________________________________________________________________________________
// ENVIRONMENT:
#define NO_PROTOCOL_DETECTED 255
#define ERROR_MARGIN 64 // [4 interrupt overlap](16*4) = 64µs
#define ERROR_BIT 254


volatile uint8_t  DETECTED_PROTOCOL = NO_PROTOCOL_DETECTED;
volatile uint64_t _SAVED_DATA_;

#define STF_LEADING_PULSE_FACTOR    0
#define STF_TAILING_PULSE_FACTOR    1
#define DATA_LENGTH                 2
#define DATA_STARTING_PULSE         3
#define D0_LEADING_PULSE_STATE      4
#define D0_LEADING_PULSE_FACTOR     5
#define D0_TAILING_PULSE_FACTOR     6
#define D1_LEADING_PULSE_FACTOR     7
#define D1_TAILING_PULSE_FACTOR     8
#define PROTOCOL_FULL_LENGTH        9
#define END_LEADING_PULSE_FACTOR    10
#define END_TAILING_PULSE_FACTOR    11
#define REPEATE_INTERVAL_FACTOR     12

//________________________________________________________________________________________________________________________________________
// PROTOCOLS:
#define NUM_SUPPORTED_PROTOCOLS 5

#define NEC_PULSE_TIME     560
#define SAMSUNG_PULSE_TIME 560
#define JAPAN_PULSE_TIME   420
#define SIRCS_PULSE_TIME   600
#define RC5_PULSE_TIME     889

const uint8_t  NEC_Data[]      = {16, 8,  8, 35,  0, 1, 1, 1, 3,  68, 1, 1, 193};
const uint8_t  SAMSUNG_Data[]  = { 8, 8,  8, 35,  0, 1, 1, 1, 3,  68, 1, 1, 107};
const uint8_t  JAPAN_Data[]    = { 8, 4,  8, 67,  0, 1, 1, 1, 4,  98, 0, 0, 100};
const uint8_t  SIRCS_Data[]    = { 4, 1,  7,  3,  0, 1, 1, 2, 1,  26, 0, 0,  75};
const uint8_t  RC5_Data[]      = { 1, 1,  6, 17,  1, 1, 1, 1, 1,  28, 0, 0, 128};

const uint16_t SUPPORTED_PROTOCOLS_PULSE_TIME[NUM_SUPPORTED_PROTOCOLS] = {
  NEC_PULSE_TIME,
  SAMSUNG_PULSE_TIME,
  JAPAN_PULSE_TIME,
  SIRCS_PULSE_TIME,
  RC5_PULSE_TIME,
};

const uint8_t* SUPPORTED_PROTOCOLS_DATA[NUM_SUPPORTED_PROTOCOLS] = {
  NEC_Data,
  SAMSUNG_Data,
  JAPAN_Data,
  SIRCS_Data,
  RC5_Data,
};

// SET AFTER A PROTOCOL IS SELECTED:
volatile uint16_t D0_LeadingPulse_Duration;
volatile uint16_t D0_TailingPulse_Duration;
volatile uint16_t D1_LeadingPulse_Duration;
volatile uint16_t D1_TailingPulse_Duration;
volatile uint8_t  D0_LeadingPulse_State;
volatile uint8_t  DataStartingPulse;
volatile uint8_t  DataEndingPulse;
volatile uint8_t  LastPulse;
volatile int32_t RepeatedSignalInterval; //To stop at start (no protocol detected yet)

void protocolDetection(uint16_t STF_FPD, uint16_t STF_SPD){
  for (uint8_t i = 0; i < NUM_SUPPORTED_PROTOCOLS; i++){
    volatile uint16_t protocol_PulseTime  = SUPPORTED_PROTOCOLS_PULSE_TIME[i];
    volatile const uint8_t* protocol_Data  = SUPPORTED_PROTOCOLS_DATA[i];
    volatile int16_t pusleDuration = (protocol_PulseTime * protocol_Data[STF_LEADING_PULSE_FACTOR]) - (STF_FPD * 16);

    if (abs(pusleDuration) <= ERROR_MARGIN){
      pusleDuration = (protocol_PulseTime * protocol_Data[STF_TAILING_PULSE_FACTOR]) - (STF_SPD * 16);
      if (abs(pusleDuration) <= ERROR_MARGIN){
        DETECTED_PROTOCOL = i;
        protocolEnvironmentVariablesSetup(protocol_PulseTime, protocol_Data);
        return;
      }
    }
  }
}

void protocolEnvironmentVariablesSetup(volatile const uint16_t DetectedProtocol_PulseTime, volatile const uint8_t* protocol_Data){
  D0_LeadingPulse_Duration = protocol_Data[D0_LEADING_PULSE_FACTOR] * DetectedProtocol_PulseTime;
  D0_TailingPulse_Duration = protocol_Data[D0_TAILING_PULSE_FACTOR] * DetectedProtocol_PulseTime;
  D1_LeadingPulse_Duration = protocol_Data[D1_LEADING_PULSE_FACTOR] * DetectedProtocol_PulseTime;
  D1_TailingPulse_Duration = protocol_Data[D1_TAILING_PULSE_FACTOR] * DetectedProtocol_PulseTime;
  D0_LeadingPulse_State = protocol_Data[D0_LEADING_PULSE_STATE];
  DataStartingPulse = protocol_Data[DATA_STARTING_PULSE];
  DataEndingPulse = DataStartingPulse + (protocol_Data[DATA_LENGTH] * 2);
  LastPulse = protocol_Data[PROTOCOL_FULL_LENGTH];
  RepeatedSignalInterval = ((int32_t) protocol_Data[REPEATE_INTERVAL_FACTOR]) * (int32_t) DetectedProtocol_PulseTime;
}

//________________________________________________________________________________________________________________________________________
// SIGNAL:
volatile int32_t timeFromSTF;
volatile uint16_t pulse = 0;
volatile uint16_t firstPulseDuration = 0;
volatile bool isRepeatedSignal = false;
volatile byte _DATA_;

ISR(PCINT2_vect) {
  volatile const uint16_t CURRENT_TIME = TCNT1; timeFromSTF += CURRENT_TIME; TCNT1 = 0; pulse++;
  if (DETECTED_PROTOCOL == NO_PROTOCOL_DETECTED){
    if (pulse == 1) {repeatedSignalCheck(); return;}
    if (pulse == 2) {firstPulseDuration = CURRENT_TIME;}
    if (pulse == 3) {protocolDetection(firstPulseDuration, CURRENT_TIME); _DATA_ = 0;}
    return;
  } else {
    if (pulse >= DataStartingPulse && pulse <= DataEndingPulse) { // 35 (low first interr data)
    if (pulse % 2 == 0) {
      firstPulseDuration = CURRENT_TIME;
    } else {
        if (pulse != DataStartingPulse) { // firstTime no action
          determineDataBit(firstPulseDuration, CURRENT_TIME) ? decode_DATA(1) : decode_DATA(0);
        } else {
          firstPulseDuration = 0; // Reset firstPulseDuration when pulse equals 35
          //first interrupt of data
        }
        return;
      }
    }
  }

  if (pulse == LastPulse) {
    //DONE//
    pulse = 0;
    save_DATA();
    DETECTED_PROTOCOL = NO_PROTOCOL_DETECTED;
  }
}

bool repeatedSignalCheck(){
  if (_DATA_ == 0){return true;}
  volatile int32_t signalDuration = RepeatedSignalInterval - timeFromSTF;
  timeFromSTF = 0;
  if (signalDuration > ERROR_MARGIN && abs(signalDuration) <= (ERROR_MARGIN * 50)){ //3200µs
    timeout(abs(signalDuration));
    save_DATA();
    return true;
  }
  return false;
}

//________________________________________________________________________________________________________________________________________
// FUNCTIONALITIES:

void decode_DATA(byte bitValue) {
  _DATA_ = (_DATA_ >> 1) | ((bitValue) << 7);
}

static void save_DATA() {
  _SAVED_DATA_ <<= 8; // Shift _SAVED_DATA_ by 8 bits to make room for the new byte
  _SAVED_DATA_ |= _DATA_; // OR the new data with _SAVED_DATA_
}

uint8_t determineDataBit(uint16_t DX_FPD, uint16_t DX_SPD){
  volatile int16_t pulseDuration = D0_LeadingPulse_Duration - (DX_FPD * 16); //from -32,768 to 32,767 inclusively. firstPulse

  if ((pinState() == D0_LeadingPulse_State) && abs(pulseDuration) <= ERROR_MARGIN){
    pulseDuration = D0_TailingPulse_Duration - (DX_SPD * 16); //secondPulse
    if (abs(pulseDuration) <= ERROR_MARGIN){
      return 0;
    }
  }
  pulseDuration = D1_LeadingPulse_Duration - (DX_FPD * 16);   //firstPulse
  if (abs(pulseDuration) <= ERROR_MARGIN){
    pulseDuration = D1_TailingPulse_Duration - (DX_SPD * 16); //secondPulse
    if (abs(pulseDuration) <= ERROR_MARGIN){
      return 1;
    }
  }
  return ERROR_BIT; //ERROR
}

bool pinState(){return (PIND & (1 << PD2)) != 0;}

//________________________________________________________________________________________________________________________________________
// SETUP:
void timerSetup() {
  TCCR1A = 0;  // Clear Timer/Counter 1 Control Register A
  TCCR1B = 0;  // Clear Timer/Counter 1 Control Register B
  TCNT1 = 0;   // Clear Timer/Counter 1
  TCCR1B |= (1 << CS12);  // PresDurationer 256 (1 -> 16µs)
  OCR1A = 65535;  // Set the compare match value (1,04856s) MAX
  TIMSK1 |= (1 << OCIE1A); // Enable timer interrupt on compare match
  TCCR1A |= (1 << WGM12); // Set the Waveform Generation mode (WGM) to CTC mode
}

ISR(TIMER1_COMPA_vect) {
  PCMSK2 |= (1 << PCINT18);
  OCR1A = 65535;
}

void timeout(int32_t timeLeft){
  PCMSK2 &= ~(1 << PCINT18);
  TCNT1 = 0;
  OCR1A = timeLeft / 16; //all timeout
  _DATA_ = 0;
}

void outputSetup(){
  DDRD &= ~(1 << DDD2);     // Set Pin 2 as input (clear bit 2 in DDRD)
  PORTD |= (1 << PORTD2);   // Enable internal pull-up resistor on Pin 2 (set bit 2 in PORTD)
  PCICR |= (1 << PCIE2);    // Enable Pin Change Interrupt for PCINT23..16 (PCICR bit 2)
  PCMSK2 |= (1 << PCINT18); // Enable interrupt for Pin Change Enable Mask Register 2, bit 2 (PCINT18)
}

//________________________________________________________________________________________________________________________________________
//DRIVER CODE:
int main(void) {
  sei();
  timerSetup();
  outputSetup();
  while(1) {}
  return 0;
}
