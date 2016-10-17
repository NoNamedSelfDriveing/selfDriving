#include <wiringPi.h>
#include <cstdio>
#include <softPwm.h>
#include <iostream>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/utsname.h>		// added ver.2
#include <netdb.h>				// added ver.2
#include <string.h>
#include <unistd.h>

#include <thread>

#define SIZE sizeof(struct sockaddr_in)

#define SAFEDIS 20

#define TRIG 26
#define ECHO 22

#define SPEED 40

#define DC_PULSE_OUT 5
#define DC_A 27
#define DC_B 28

#define SERVO 29

#define FRONT 0
#define BACK 1

#define _GO 1
#define _BACK 2
#define _LEFT 4
#define _RIGHT 8

#define CENTER 1350
#define RIGHT 1000
#define LEFT 1650

char log[1024];
unsigned int i;

int FLAG;
long startTime, travelTime;
int distance;

void    insert(int, int);
void    stop();
void    set_direct(int);
void    rotateServo(int);
int     getCM();
void    threadService();

void closesock(int sig);

int sockfd_connect;

int main(int argc, char *argv[]){
    if(argc < 2){
        fprintf(stderr, "Usage : %s [PORT]]n", argv[0]);
        exit(1);
    }

    int sockfd;
    char tmp[50];
    struct sockaddr_in server = {AF_INET, htons(atoi(argv[1])), INADDR_ANY};
    struct sockaddr_in client;			// added ver.2
    int client_len = SIZE;				// added ver.2

    wiringPiSetup();

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
        printf("fail to call socket\n");
        exit(1);
    }

    if(bind(sockfd, (struct sockaddr *)&server, SIZE) == -1){
        printf("fail to call bind\n");
        exit(2);
    }

    if(listen(sockfd, 1) == -1){
        printf("fail to call listen()\n");
        exit(3);
    }

    std::cout << "Go Straight::NN" << std::endl;

    softPwmCreate(DC_PULSE_OUT, 0, 100);

    pinMode(DC_A, OUTPUT);
    pinMode(DC_B, OUTPUT);
    pinMode(SERVO, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(TRIG, OUTPUT);

    std::thread t1(&threadService);

    set_direct(FRONT);

    int Cont_command;
    char msg[1024];
    char *Cent_msg, *Sum_msg, *Cont_msg;

    while(1){
        if((sockfd_connect = accept(sockfd, NULL,NULL)) < 0){
            printf("fail to call accept()\n");
            exit(4);
        }

        printf("accepted\n");
        while(recv(sockfd_connect, &msg, 1024, 0) > 0){
            Cont_msg = strtok(msg,",");

            Cont_command = atoi(Cont_msg);

            std::cout << msg << FLAG << std::endl;
            if((Cont_command & _GO) && !(FLAG)){
                set_direct(FRONT);
                if(Cont_command & _LEFT) 
                {
                    rotateServo(LEFT);
                    softPwmWrite(DC_PULSE_OUT, SPEED + 20);
                }
                else if(Cont_command & _RIGHT) 
                {
                    rotateServo(RIGHT);
                    softPwmWrite(DC_PULSE_OUT, SPEED + 20);
                }
                else
                {
                    rotateServo(CENTER);
                    softPwmWrite(DC_PULSE_OUT, SPEED);
                }
            }
            else if(Cont_command & _BACK){
                set_direct(BACK);
                if(Cont_command & _LEFT) 
                {
                    rotateServo(LEFT);
                    softPwmWrite(DC_PULSE_OUT, SPEED + 20);
                }
                else if(Cont_command & _RIGHT) 
                {
                    rotateServo(RIGHT);
                    softPwmWrite(DC_PULSE_OUT, SPEED + 20);
                }
                else 
                {
                    rotateServo(CENTER);
                    softPwmWrite(DC_PULSE_OUT, SPEED);
                }
            }
            else stop();
        }
        printf("close(sockfd_connect)\n");
        close(sockfd_connect);
    }
}

void closesock(int sig){
    close(sockfd_connect);
    printf("connection is lost\n");
    exit(0);
}

void stop(){
    digitalWrite(DC_A, 1);
    digitalWrite(DC_B, 1);
}

void set_direct(int direct){
    if(direct == 1){
        digitalWrite(DC_A, 0);
        digitalWrite(DC_B, 1);
    }
    else{
        digitalWrite(DC_A, 1);
        digitalWrite(DC_B, 0);
    }
}

void rotateServo(int time)
{
    digitalWrite(SERVO, HIGH);
    delayMicroseconds(time);
    digitalWrite(SERVO, LOW);
    delayMicroseconds(23);
}

int getCM()
{
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(20);
    digitalWrite(TRIG, LOW);

    while(digitalRead(ECHO) == LOW);

    startTime = micros();
    while(digitalRead(ECHO) == HIGH);
    travelTime = micros() - startTime;

    distance = travelTime / 58;

    return distance;
}

void threadService()
{
    while(1)
    {
        if(getCM() > SAFEDIS) FLAG = 0;
        else FLAG = 1;
    }
}
