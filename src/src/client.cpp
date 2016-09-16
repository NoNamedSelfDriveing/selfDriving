#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <wiringPi.h>
#include <softPwm.h>

#include <thread>
#include<opencv2/opencv.hpp>

#define FL_PULSE_OUT 4
#define FR_PULSE_OUT 5

#define RB 24
#define RF 25
#define LB 27
#define LF 28

#define HIGH 1
#define LOW 0

#define GO 1
#define BACK 2
#define LEFT 4
#define RIGHT 8

using namespace std;
using namespace cv;
/*
void insert(int left, int right){
    softPwmWrite(FL_PULSE_OUT, left);
    softPwmWrite(FR_PULSE_OUT, right);
}

void stop(){
    insert(0, 0);
}

void set_direct(int left, int right){
    if(left == 1){
        digitalWrite(LB, 0);
        digitalWrite(LF, 1);
    }
    else{
        digitalWrite(LB, 1);
        digitalWrite(LF, 0);
    }

    if(right == 1){
        digitalWrite(RB, 0);
        digitalWrite(RF, 1);
    }
    else{
        digitalWrite(RB, 1);
        digitalWrite(RF, 0);
    }

}

void recv_command(int port){
    int command_sock, sockfd;
    struct sockaddr_in rpi_addr = {AF_INET, htons(port+1), INADDR_ANY};
    struct sockaddr_in com_addr;

    int client_len = sizeof(struct sockaddr_in);
    int command;

    if((command_sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket");
        exit(1);
    }

    if(bind(command_sock, (struct sockaddr*)&rpi_addr, sizeof(struct sockaddr_in)) < 0)
    {
        perror("bind");
        exit(1);
    }

    if(listen(command_sock, 1) < 0)
    {
        perror("listen");
        exit(1);
    }

    std::cout << "Ready to receive command from PC::NN" << std::endl;

    char msg[16];
    while(1){
        if((sockfd = accept(command_sock, NULL, NULL)) < 0)
        {
            perror("accept");
            exit(1);
        }
        else
        {
            std::cout << "Accepted" << std::endl;
        }

        set_direct(HIGH, HIGH);

        while(recv(sockfd, &msg, sizeof(msg), 0))
        {
            std::cout << "receive : " << msg << std::endl;
            command = atoi(msg);

            if(command == 215){
                insert(30, 30);
            }
            else if(command > 215){
                insert(30, 10);
            }
            else if(command < 215){
                insert(10, 30);
            }
            else if(command < 0){
                stop();
            }
        }
        close(sockfd);
    }
    close(command_sock);
}
*/
int main(int argc, char **argv)
{
    int sock;
    int send_len;
    int c;
    struct sockaddr_in pc_addr;
    double width = 800;
    double height = 600;
    VideoCapture capture = atoi(argv[3]);
    Mat frame;
    vector<uchar> ibuff;
    vector<int> param = vector<int>(2);
    int sendSize = 65535;
    char buff[sendSize];

    sock = socket(AF_INET, SOCK_DGRAM, 0);

    pc_addr.sin_family = AF_INET;
    pc_addr.sin_port = htons(atoi(argv[2]));
    pc_addr.sin_addr.s_addr = inet_addr(argv[1]);

    if(!capture.isOpened()){
        perror("Capture");
        exit(1);
    }

    //jpeg compression

    param[0] = CV_IMWRITE_JPEG_QUALITY;
    param[1] = 55; //default(95) 0-100

    //std::thread t1(recv_command, atoi(argv[2]));
    while (1) {
        capture >> frame;

        imencode(".jpeg", frame, ibuff, param);
        for (int i = 0; i < ibuff.size(); i++)
        {
            buff[i]=ibuff[i];
        }

        send_len = sendto(sock, buff, ibuff.size(), 0, (struct sockaddr *)&pc_addr, sizeof(pc_addr));

        if (send_len==-1)
            perror("socket");
    }

    close(sock);
    return 0;
}
