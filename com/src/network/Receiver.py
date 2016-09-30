#-*- coding: utf-8 -*-

import socket

class Receiver:
    def __init__(self, ip, port):
        '''
        ip와 포트를 입력받아 미리 설정하고
        소켓을 생성 이미지는 UDP 서버로 커멘드는 TCP 클라이언트로 사용
        '''

        self.IP = ip
        self.PORT = int(port)

        self.img_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.commend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        '''
        이미지 소켓과 커맨드 소켓을 사용 타겟보드와 연결 시작
        이미지는 5000번 커멘드는 그것에 + 1
        '''
        self.img_sock.bind(('', self.PORT)) # 이미지 서버 바인드
        self.commend_sock.connect((self.IP, self.PORT+1))  # 명령어 서버 바인드 예정

    def receive(self):
        '''
        이미지 데이터를 받아서 데이터와 보낸 ip를 반환
        '''

        data, addr = self.img_sock.recvfrom(1024*65) # 1024 * 65 is size

        return data, addr
