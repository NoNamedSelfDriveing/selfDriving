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
#include <sys/utsname.h>    // added ver.2
#include <netdb.h>        // added ver.2
#include <string.h>
#include <unistd.h>

#include <thread>

#define SIZE sizeof(struct sockaddr_in)

#define SAFEDIS 20

#define TRIG 26
#define ECHO 22

#define SPEED 40
#define FIXSPEED 15

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
#define _CENTER 150

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
        if(argc < 2) {
                fprintf(stderr, "Usage : %s [PORT]]n", argv[0]);
                exit(1);
        }

        int sockfd;
        char tmp[50];
        struct sockaddr_in server = {AF_INET, htons(atoi(argv[1])), INADDR_ANY};
        struct sockaddr_in client;  // added ver.2
        int client_len = SIZE;    // added ver.2

        wiringPiSetup();

        if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
                printf("fail to call socket\n");
                exit(1);
        }

        if(bind(sockfd, (struct sockaddr *)&server, SIZE) == -1) {
                printf("fail to call bind\n");
                exit(2);
        }

        if(listen(sockfd, 1) == -1) {
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

        /*
            commender.addCommend(image.angle)
            commender.addCommend(image.left_angle)
            commender.addCommend(image.right_angle)
            commender.addCommend(image.x_avr)
            commender.addCommend(mlOption)
            main.py contents.
         */

        int Cont_command, Sum_angle_command;
        double Xangle_command, Left_angle_command, Right_angle_command;
        char msg[1024], Mode_command[6];
        /*
           *_command의 경우 atoi(), atof()를 통해 문자열을 변수 타입에 맞춰 넣는 변수
         */

        char *Cont_msg, *Xangle_msg, *Left_anle_msg, *Right_angle_msg, *Sum_angle_msg, *Mode_msg;

        /*
           *_msg의 경우 소켓을 통해 받은 문자열을 ',' 기준으로 파싱 저장한 변수
         */

        while(1) {
                if((sockfd_connect = accept(sockfd, NULL,NULL)) < 0) {
                        printf("fail to call accept()\n");
                        exit(4);
                }

                printf("accepted\n");
                while(recv(sockfd_connect, &msg, 1024, 0) > 0) {
                        std::cout << msg << FLAG << std::endl;

                        Cont_msg        = strtok(msg,",");
                        Xangle_msg      = strtok(NULL, ",");
                        Left_angle_msg  = strtok(NULL, ",");
                        Right_angle_msg = strtok(NULL, ",");
                        Sum_angle_msg   = strtok(NULL, ",");
                        Mode_msg        = strtok(NULL, "\0");
                        // 소켓을 통해 받은 msg를 각각의 변수에 저장

                        Cont_command = atoi(Cont_msg);
                        Left_angle_command = atof(Left_angle_msg);
                        Right_angle_command = atof(Right_angle_msg);
                        Sum_angle_command = atoi(Sum_angle_msg);
                        strcpy(Mode_command, Mode_msg);
                        // 변수에 파싱한 내용을 변수 타입에 맞게 저장, 이후 소스에서는 *_command 변수만을 사용함

                        if(!(strcmp(Mode_command, "False")) == 0)
                        {
                                if((Cont_command & _GO) && !(FLAG)) {
                                        set_direct(FRONT);
                                        if(Cont_command & _LEFT)
                                        {
                                                rotateServo(LEFT);
                                                softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                        }
                                        else if(Cont_command & _RIGHT)
                                        {
                                                rotateServo(RIGHT);
                                                softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                        }
                                        else
                                        {
                                                rotateServo(CENTER);
                                                softPwmWrite(DC_PULSE_OUT, SPEED);
                                        }
                                }
                                else if(Cont_command & _BACK) {
                                        set_direct(BACK);
                                        if(Cont_command & _LEFT)
                                        {
                                                rotateServo(LEFT);
                                                softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                        }
                                        else if(Cont_command & _RIGHT)
                                        {
                                                rotateServo(RIGHT);
                                                softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                        }
                                        else
                                        {
                                                rotateServo(CENTER);
                                                softPwmWrite(DC_PULSE_OUT, SPEED);
                                        }
                                }
                                else stop();
                        }
                        else if(!(strcmp(Msg_command, "True")) == 0)
                        {
                                if(Sum_angle_command > _CENTER)
                                {
                                        rotateServo(LEFT);
                                        softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                }
                                else if(Sum_angle_command < _CENTER)
                                {
                                        rotateServo(RIGHT);
                                        softPwmWrite(DC_PULSE_OUT, SPEED + FIXSPEED);
                                }
                                else
                                {
                                        rotateServo(CENTER);
                                        softPwmWrite(DC_PULSE_OUT, SPEED);
                                }
                        }
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
        if(direct == 1) {
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

        while(digitalRead(ECHO) == LOW) ;

        startTime = micros();
        while(digitalRead(ECHO) == HIGH) ;
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
