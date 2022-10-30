#include <SoftwareSerial.h>
// Define the data transmit/receive pins in Arduino
#define TxD 10
#define RxD 11
#define N_SERVOS 6
const int CAPACITIVE_PINS[N_SERVOS] = {2,3,4,5,6,7};
#define CAPACITIVE_THRESHOLD 5
char charChange[4];

SoftwareSerial mySerial(RxD, TxD); // RX, TX for Bluetooth


// For capacitive diffing
bool last_capacitive[N_SERVOS] = {false};

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600); // For Bluetooth
}

void loop() {
  // Serial.println(last_capacitive);
   printDiff();
//  honestPrint();
//  Serial.print(mySerial.available());
//  Serial.print('\n');
//  if (mySerial.available()) {
////    mySerial.write(Serial.read());
//      mySerial.println("hello");
//  }
  delay(100);
}

uint8_t readCapacitivePin(int pinToMeasure) {
  volatile uint8_t* port;
  volatile uint8_t* ddr;
  volatile uint8_t* pin;
  byte bitmask;
  port = portOutputRegister(digitalPinToPort(pinToMeasure));
  ddr = portModeRegister(digitalPinToPort(pinToMeasure));
  bitmask = digitalPinToBitMask(pinToMeasure);
  pin = portInputRegister(digitalPinToPort(pinToMeasure));
  *port &= ~(bitmask);
  *ddr  |= bitmask;
  delay(1);
  uint8_t SREG_old = SREG; //back up the AVR Status Register
  noInterrupts();
  *ddr &= ~(bitmask);
  *port |= bitmask;
  uint8_t cycles = 17;
  if (*pin & bitmask) {
    cycles =  0;
  } else if (*pin & bitmask) {
    cycles =  1;
  } else if (*pin & bitmask) {
    cycles =  2;
  } else if (*pin & bitmask) {
    cycles =  3;
  } else if (*pin & bitmask) {
    cycles =  4;
  } else if (*pin & bitmask) {
    cycles =  5;
  } else if (*pin & bitmask) {
    cycles =  6;
  } else if (*pin & bitmask) {
    cycles =  7;
  } else if (*pin & bitmask) {
    cycles =  8;
  } else if (*pin & bitmask) {
    cycles =  9;
  } else if (*pin & bitmask) {
    cycles = 10;
  } else if (*pin & bitmask) {
    cycles = 11;
  } else if (*pin & bitmask) {
    cycles = 12;
  } else if (*pin & bitmask) {
    cycles = 13;
  } else if (*pin & bitmask) {
    cycles = 14;
  } else if (*pin & bitmask) {
    cycles = 15;
  } else if (*pin & bitmask) {
    cycles = 16;
  }
  SREG = SREG_old;
  *port &= ~(bitmask);
  *ddr  |= bitmask;
  return cycles;
}

void printDiff() {
  for (int i = 0; i < N_SERVOS; i ++) {
    uint8_t reading = readCapacitivePin(CAPACITIVE_PINS[i]);
    bool is_finger_down = reading >= CAPACITIVE_THRESHOLD;
    if (is_finger_down != last_capacitive[i]) {
      last_capacitive[i] = is_finger_down;
      Serial.print('\n');
//      Serial.print(i);
      String change = String(i);
      if (is_finger_down) {
//        Serial.print('_');
        change += '_';
      } else {
//        Serial.print('^');
        change += '^';
      }
      change.toCharArray(charChange, 4);
      Serial.println(change);
      if (mySerial.available()) {
        mySerial.write(charChange);
      }
    }
  }
}

void honestPrint() {
  for (int i = 0; i < N_SERVOS; i ++) {
    uint8_t reading = readCapacitivePin(CAPACITIVE_PINS[i]);
    Serial.print("C");
    Serial.print(i);
    Serial.print(" = ");
    Serial.print(reading);
    Serial.print('\t');
  }
  Serial.println();
}
