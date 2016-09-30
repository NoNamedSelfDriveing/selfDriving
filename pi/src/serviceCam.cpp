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

/* set Server */
#define MAX_CLIENT 5

/*  
 *  about MAX_CLIENT
 *
 *  Server can listen about 'MAX_CLIENT'
 */

void openServer(int, struct sockaddr_in, char);

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

int port;

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    if(argc < 3)
    {
        cout << "Usage: " << argv[0] << " [PORT] [Camera]" << endl;
        exit(4);
    }
    port = atoi(argv[1]);

    struct sockaddr_in frame_server, msg_server;
    int frame_sock, msg_sock;

    frame_server.sin_family = AF_INET;
    frame_server.sin_addr.s_addr = inet_addr("10.42.0.225");
    frame_server.sin_port = htons(atoi(argv[1]));
    openServer(frame_sock, frame_server, 'U');

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
            cout << "Client Non" << endl;
        }
    }

    close(frame_sock);
    return 0;
}

void openServer(int sock, struct sockaddr_in server_addr, char sock_opt)
{
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
        cout << sock_opt << endl;
        perror(":bind");
        exit(2);
    }

    if(sock_opt == 'T' && listen(sock, MAX_CLIENT) < 0)
    {
        cout << sock_opt << endl;
        perror(":listen");
        exit(2);
    }
}
