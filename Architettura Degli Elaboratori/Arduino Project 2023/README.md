```
void outputSetUp(){
  DDRD   &= ~(1 << DDD2);    // Imposta il Pin 2 come input (DDRD bit 2 a 0)
  PORTD  |= (1 << PORTD2);   // Abilita la resistenza di pull-up interna sul Pin 2 (PORTD bit 2 a 1)
  PCICR  |= (1 << PCIE2);    // Abilita l'interrupt Pin Change 2 (PCICR bit 2 a 1)
  PCMSK2 |= (1 << PCINT18);  // Abilita l'interrupt per il Pin 2 (PCMSK2 bit 2 a 1)
}

```
