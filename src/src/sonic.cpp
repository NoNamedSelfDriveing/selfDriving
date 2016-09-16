#include <iostream>
#include <ctime>
#include <cstdio>

#include <math.h>
#include <unistd.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <time.h>

#define TRIG 23
#define ECHO 29
#define OUTP 24

int main(){
		time_t startTime, endTime;
		double distance;

		if ( wiringPiSetup()!=0 ){
				perror("wiringPi setup");
				exit(1);
		}

		pinMode(TRIG, OUTPUT);
		pinMode(ECHO, INPUT);
		pinMode(OUTP, OUTPUT);

		digitalWrite(TRIG, FALSE);

		digitalWrite(TRIG, TRUE);
		usleep(10);
		digitalWrite(TRIG, FALSE);

		while ( digitalRead(ECHO) == 0 ){
			std::cout << "W" << std::endl;
			startTime = time(0);		
		}
		while ( digitalRead(ECHO) == 1 ){
			std::cout << "R" << std::endl;
			endTime = time(0);
		}

		distance = double((endTime - startTime) * 17150);
		distance = round(distance);

		if ( distance > 10 ){
				digitalWrite(OUTP, TRUE);	
		} else {
				digitalWrite(OUTP, FALSE);
		}
}
