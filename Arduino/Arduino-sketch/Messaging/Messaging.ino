#include "Parser.h"       // библиотека парсера
#include "AsyncStream.h"  // асинхронное чтение сериал
AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ

#define LIGHT1 9
#define FAN 10
#define MOVE 11
#define GAS 8

void setup() {
  Serial.begin(115200);
  pinMode(LIGHT1, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(MOVE, INPUT);
  pinMode(GAS, INPUT);
}

void loop() {
  static uint32_t tmr = 0;
  if(millis() - tmr > 100){
    tmr = millis();
    Serial.print(0);
    Serial.print(',');
    Serial.println(digitalRead(MOVE));
//
//    tmr = millis();
//    Serial.print(1);
//    Serial.print(',');
//    Serial.println(digitalRead(GAS));
  }
  parsing();

  // для отправки нескольких интов
  /*
    int packet[3];
    packet[0] = 255;
    packet[1] = 255;
    packet[2] = 255;
    sendPacket(0, packet, 3);
  */
}

// функция для отправки пакета на ПК
void sendPacket(int key, int* data, int amount) {
  Serial.print(key);
  Serial.print(',');
  for (int i = 0; i < amount; i++) {
    Serial.print(data[i]);
    if (i != amount - 1) Serial.print(',');
  }
  Serial.print('\n');
}

// функция парсинга, опрашивать в лупе
void parsing() {
  if (serial.available()) {
    Parser data(serial.buf, ',');  // отдаём парсеру
    int ints[10];           // массив для численных данных
    data.parseInts(ints);   // парсим в него

    switch (ints[0]) {      // свитч по ключу
      case 0: // NOT USE!!!
        break;
      case 1: digitalWrite(LIGHT1, ints[1]);
        break;
      case 2: digitalWrite(FAN, ints[1]);
        break;
      case 3:
        break;
    }
  }
}
