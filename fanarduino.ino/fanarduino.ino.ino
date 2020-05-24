
#include <FastLED.h>
CRGB leds[10][12];
char record[500];
int recount = 0;
void setup() {
  FastLED.addLeds<NEOPIXEL, 0>(leds[0], 12);
  FastLED.addLeds<NEOPIXEL, 1>(leds[1], 12);
  FastLED.addLeds<NEOPIXEL, 2>(leds[2], 12);
  FastLED.addLeds<NEOPIXEL, 3>(leds[3], 12);
  FastLED.addLeds<NEOPIXEL, 4>(leds[4], 12);
  FastLED.addLeds<NEOPIXEL, 5>(leds[5], 12);
  FastLED.addLeds<NEOPIXEL, 6>(leds[6], 12);
  FastLED.addLeds<NEOPIXEL, 7>(leds[7], 12);
  FastLED.addLeds<NEOPIXEL, 8>(leds[8], 12);
  FastLED.addLeds<NEOPIXEL, 9>(leds[9], 12);
  Serial.begin(115200);

}
char colors[3][12];
void loop() {

  if (Serial.available() > 0) {
    sendpics();

  }

}


void sendpics() {
  int counter = 0;
  int subcount = 0;
  int rgb[3];
  char c = Serial.read();
  if (c == '?') {
    Serial.println("!");
    return;
  }
  if (c == '[') {
    while (Serial.available() == 0) {
    }
    char pin = Serial.read();
    int pinint = chartoint(pin);
    if (pinint >= 0) {
      if (pinint <= 9) {
        while (Serial.available() == 0) {
        }
        char exi = Serial.read();
        if (exi == ']') {
          while (counter < 36) {
            while (Serial.available() == 0) {
            }
            char num = Serial.read();
            rgb[subcount] = toNum(num);
            subcount++;
            if (subcount > 2) {
              subcount = 0;
              leds[pinint][int(counter / 3)] = CRGB(rgb[0], rgb[1], rgb[2]);
            }
            counter++;
          }
          FastLED.show();
          delay(10);
          return;
        }

      }
    }

  }
  return;
}



int chartoint(char c) {
  switch (c) {
    case '0':
      return 0;
    case '1':
      return 1;
    case '2':
      return 2;
    case '3':
      return 3;
    case '4':
      return 4;
    case '5':
      return 5;
    case '6':
      return 6;
    case '7':
      return 7;
    case '8':
      return 8;
    case '9':
      return 9;
  }
}


int toNum(char s)
{
  switch (s) {
    case '0':
      return 0;
    case '1':
      return 17;
    case '2':
      return 34;
    case '3':
      return 51;
    case '4':
      return 68;
    case '5':
      return 85;
    case '6':
      return 102;
    case '7':
      return 119;
    case '8':
      return 136;
    case '9':
      return 153;
    case 'a':
      return 170;
    case 'b':
      return 187;
    case 'c':
      return 204;
    case 'd':
      return 221;
    case 'e':
      return 238;
    case 'f':
      return 255;
  }
}
