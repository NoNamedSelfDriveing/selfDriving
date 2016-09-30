#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#include<opencv2/opencv.hpp>


using namespace std;
using namespace cv;

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

    if(sock < 0)
    {
        perror("socket");
        exit(1);
    }

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
