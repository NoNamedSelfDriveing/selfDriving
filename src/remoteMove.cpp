/*
 *
 * Author : potato
 *
 * Date : 7th. September. 2016
 *
 * E-mail : evtktma@gmail.com
 * - If you have any question about source,
 *   then I'll answer about this code.
 * - Please send email to me.
 *
 * Hardware :
 *    Raspberry PI 3 B+
 *    Servo Motor   =   HS-311
 *    DC Motor      =   I didn't know yet...
 *    Pi Cam
 *    //MPU sensor    =   MPU9250
 */

#include <wiringPi.h>
#include <softPwm.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#include <string.h>
#include <unistd.h>
#include <iostream>

#include <opencv2/opencv.hpp>
#include <thread>

#define SIZE sizeof(struct sockaddr_in)

/* Set DC motor */
#define DC_SPEED 23
#define DC_DIRECTION_A 24
#define DC_DIRECTION_B 25

/* Set Direction */
#define SERVO_MOTOR 1

/* set Server */
#define MAX_CLIENT 5


/* Information about <Define> */

/*
 *  about DC_MOTOR_*
 *
 *  Front : DC_DIR_A == 1 & DC_DIR_B == 0
 *
 *  Back : DC_DIR_A == 0 & DC_DIR_B == 1
 *
 */

/*
 * about SERVO_MOTOR
 *
 *    write HIGH on SERVO pin for x microseconds
 *
 *    ex)
 *    loop(int time = 1350)
 *    {
 *        digitalWrite(SERVO_MOTOR, HIGH);
 *        delayMicroseconds(time);
 *        digitalWrite(SERVO_MOTOR, LOW);
 *        delayMicroseconds(23);
 *    }
 *
 *    Go straight : 1350
 *
 *    Turn Left : 1750
 *
 *    Turn Right : 950
 */

/*  
 *  about MAX_CLIENT
 *
 *  Server can listen about 'MAX_CLIENT'
 */


void msgControl(int);
void openServer(int, struct sockaddr_in, char);
void setGPIO(void);

/*
 * void msgControl(sock)
 * 
 * create softPWM
 * loop()
 * {
 *      receive Message
 *      parse Message
 *      as Message value, control DC and Servo motor
 * }
 *
 */

/*
 * void openServer(sock, server_address, option)
 *
 * sock = socket()
 * bind(server)
 * listen(MAX_CLIENT)
 *
 */

/* 
 * void set GPIO(void)
 *
 * SERVO_MOTOR, OUTPUT
 * DC_SPEED, OUTPUT
 * DC_DIRECTION_A, OUTPUT
 * DC_DIRECTION_B, OUTPUT
 *
 */

int port;

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    cout << "Start remoteMove Routine" << endl;

    if(argc < 3)
    {
        cout << "Usage: " << argv[0] << " [PORT] [Camera]" << endl;
        exit(4);
    }
    port = atoi(argv[1]);
    setGPIO();  // wiringPi setup and pin mode set

    struct sockaddr_in frame_server, msg_server;
    int frame_sock, msg_sock;

    openServer(frame_sock, frame_server, 'U');
    openServer(msg_sock, msg_server, 'T');

    // thread(msg)

    int send_len, i;
    VideoCapture capture = atoi(argv[2]);
    Mat frame;
    vector<uchar> ibuff;
    vector<int> param = vector<int>(2);
    int sendSize = 65535;
    char buff[sendSize];

    if(!capture.isOpened())
    {
        perror("Open Capture");
        exit(3);
    }

    param[0] = CV_IMWRITE_JPEG_QUALITY;
    param[1] = 55;  //default(95) 0 - 100

    while(1)
    {
        capture >> frame;

        imencode(".jpeg", frame, ibuff, param);
        for(i = 0; i< ibuff.size(); i++)
        {
            buff[i] = ibuff[i];
        }

        send_len = sendto(frame_sock, buff, ibuff.size(), 0, (struct sockaddr*)&frame_server, SIZE);

        if(send_len < 0)
        {
            perror("socket");
        }
    }

    close(frame_sock);
    return 0;
}

void setGPIO(void)
{
    wiringPiSetup();    //It helps you to use wiringPi GPIO pins.

    pinMode(SERVO_MOTOR, OUTPUT);
    pinMode(DC_DIRECTION_A, OUTPUT);
    pinMode(DC_DIRECTION_B, OUTPUT);
}

void openServer(int sock, struct sockaddr_in server_addr, char sock_opt)
{
    server_addr = {AF_INET, htons(port), INADDR_ANY};
    switch(sock_opt){
        case 'T':
            if( (sock = socket(AF_INET, SOCK_STREAM, 0)) < 0 )
            {
                perror("socket");
                exit(2);
            }
            break;

        case 'U':
            if( (sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
            {
                perror("socket");
                exit(2);
            }
            break;

        default:
            cout << "Sock option is wrong" << endl;
            exit(2);
            break;
    }
    
    if(bind(sock, (struct sockaddr*)&server_addr, SIZE) < 0)
    {
        perror("bind");
        exit(2);
    }

    if(listen(sock, MAX_CLIENT) < 0)
    {
        perror("listen");
        exit(2);
    }
}

void msgControl(int sock)
{
    int connect_sock;
    int Cont_command;
    char msg[1024];
    char *cont_msg, *cont_command;

    softPwmCreate(DC_SPEED, 50, 100);

    while(1)
    {
    }
}
