#-*- coding: utf-8 -*-

import pygame

class Commender:
    def __init__(self):
        '''
        기본적인 커맨드 변수 생성과
        입력받을 창을 생성
        '''
        self.__w__ = False
        self.__s__ = False
        self.__a__ = False
        self.__d__ = False

        self.__commend__ = ""

        pygame.init()
        pygame.display.set_mode((300, 300))
        key = pygame.key.get_pressed()

    def printCommend(self):
        '''
        현재까지 연결된 명령어 출력
        '''

        print "commend is " + self.__commend__

    def setCommendH(self):
        '''
        사용자가 운전을 하는 부분
        w s a d로 이동을 조작
        입력한 조작을 str타입으로 변환하여 commend를 set한다.
        '''

        input_key = 0

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.__w__ = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.__w__ = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.__s__ = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:
                self.__s__ = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.__a__ = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.__a__ = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.__d__ = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.__d__ = False

        if self.__w__:
            input_key |= 1

        if self.__s__:
            input_key |= 2

        if self.__a__:
            input_key |= 4

        if self.__d__:
            input_key |= 8

        commend = str(input_key)
        self.__commend__ = commend

    def setCommendM(self, commend):
        '''
        TensorFlow가 처리한 결과를 str로 변환하여
        커멘드를 set한다.
        '''
        self.__commend__ = str(commend)

    def addCommend(self, commend):
        '''
        부가적인 명령어들을 set한 명령어에 연장한다
        '''
        self.__commend__ = self.__commend__ + "," + str(commend)

    def endCommend(self):
        '''
        c언어로 작성된 어플리케이션과 통신함으로 NULL문자를 넣어 문자의 종료를 알린다.
        '''

        self.__commend__ = self.__commend__ + "\0"

    def sendCommend(self, sock, addr):
        '''
        해당 TCP소켓을 이용해 명령어를 전송한다.
        '''
        sock.send(self.__commend__)

    def getCommend(self):
        '''
        지금의 명령어를 반환한다.
        '''

        return self.__commend__
