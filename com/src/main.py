#-*- coding: utf-8 -*-

import os
import cv2
import sys
import tensorflow as tf
import time
from datetime import datetime

sys.path.insert(0,'./ml')               # 뉴럴넷 관련 클래스 모음
sys.path.insert(0,'./network')          # 전송 관련 모음
sys.path.insert(0,'./process')          # data 처리 클래스 모음
sys.path.insert(0,'./commend')          # 커맨드 처리 클래스 모음
sys.path.insert(0,'./sms')              # sms 전송 클래스 모음

from Model      import Model
from Commender  import Commender
from Receiver   import Receiver
from Image      import Image
from Manager    import Manager

def str2bool(v):
  return v.lower() in ("true", "t")

if __name__ == '__main__':
    receiver    = Receiver(sys.argv[1], sys.argv[2])    # 이미지 수신 객체 ip, port
    image       = Image()                               # 이미지 처리 & 커맨드에 들어갈 요소 생성 객체
    commender   = Commender()                           # 커맨드 생성 & 전송 객체
    model       = Model()                               # tensorflow 모델 객체
    sms         = Manager('id', 'pw', '송신자 번호')      # sms 송신 관련 객체

    receiver.start() # 서버 시작

    mlOption = False

    timeSize = 19 # log 이름에 사용될 길이
    logdate = str(datetime.now())[:timeSize] # yyyy-mm-dd hh:mm:ss

    datcation = "./data/" # data 폴더 위치
    logcation = datcation + "log/" # log 폴더 위치
    imgcation = datcation + "img/" + logdate + "/" # 이미지 저장할 폴더 위치

    if not os.path.isdir(datcation):
        os.mkdir(datcation)

    if not os.path.isdir(logcation):
        os.mkdir(logcation)

    if not os.path.isdir(imgcation):
        os.mkdir(imgcation)

    logger = open(logcation + logdate +'.txt', 'w')
    # data 저장 위치 확인 및 생성

    count = 0  # 프레임 카운트
    commend = 0

    """
    print "wait 10sec"
    time.sleep(10)
    """

    with tf.Session() as sess:
        # you need to initialize all variables
        tf.initialize_all_variables().run()
        model.loadLearning(sess)

        while True:
            '''
            데이터 받고 Tensorflow에서 다음 명령어 예측
            사용자 조작값 설정하고 핸들(스페이스) 체크
            10프레임 받고 핸들 그대로 눌리지 않았다면 예측된 명령어로
            자동차에게 전달
            '''
            data, addr  = receiver.receive()
            image.splitImg(data)
            image.setImgInfo()
            data = cv2.resize(image.getImg(),(28,28))
            # 데이터 수신

            label = sess.run(model.predict_op,
            feed_dict={model.X: [data], model.p_keep_conv: 1, model.p_keep_hidden: 1})

            if(label[0] == 0):
                commend = 1
            elif(label[0] == 1):
                commend = 5
            elif(label[0] == 2):
                commend = 9
            else:
                commend = 0

            print "com     is " + str(commend)
            # 딥러닝 예측

            commender.setCommendH() # 사용자 조작값 설정

            key = int(commender.getCommend())
            if (key & 0x10): #핸들을 잡고있는 경우
                mlOption = False
            else:
                mlOption = True


            if mlOption == True:
                commender.setCommendM(commend)
                # 딥러닝 예측값 설정

                if sms.issent == False:
                    sms.sendSMS()
                    sms.issent = True
                #sms 발송


            commender.addCommend(mlOption)
            commender.addCommend(image.x_center)
            commender.addCommend(image.left_angle)
            commender.addCommend(image.right_angle)
            commender.addCommend(image.x_avr)
            # 체크 필요

            commender.endCommend()
            commender.sendCommend(receiver.commend_sock, receiver.commend_sock)
            commender.printCommend()
            # 명령어 전송

            img = cv2.resize(image.getImg(), (28, 28))
            cv2.imwrite(imgcation + str(count) + ".png", img)
            log = commender.getCommend()+"\n"
            logger.write(log)
            # 로그 저장

            cv2.imshow('image', image.getImg())
            cv2.imshow('image2',image.getCanny())
            # 이미지 프레임 출력

            count += 1

            if cv2.waitKey(30) == 1048603:
                logger.close()
                sys.exit(0)
