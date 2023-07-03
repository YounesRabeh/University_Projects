``` 
void outputSetUp(){
  DDRD   &= ~(1 << DDD2);   
  PORTD  |= (1 << PORTD2);   
  PCICR  |= (1 << PCIE2);    
  PCMSK2 |= (1 << PCINT18);  
}

```
