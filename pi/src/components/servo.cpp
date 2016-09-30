#include <wiringPi.h> //wiringPi.h 선언
#include <stdio.h>
#include <stdlib.h>
#include <softPwm.h>
#include <iostream>

int main (int argc, char *argv[])
{
    wiringPiSetup();

    pinMode(29, OUTPUT);

    int i;
    int arg = 0;
    while(1)
    {
        scanf("%d", &arg);
        for(i = 0; i < 100; i++)
        {
            digitalWrite(29, HIGH);
            delayMicroseconds(arg);
            digitalWrite(29, LOW);
            delay(30);
        }
    }
}
