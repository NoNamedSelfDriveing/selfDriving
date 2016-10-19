#-*- coding: utf-8 -*-

import numpy as np
import cv2
import math

class Image:
    def __init__(self):
        '''
        이미지와 관련된 처리를 저장하는 변수를 생성한다.
        '''

        self.__img__ = 0

        self.__canny__ = 0
        self.__left_canny__ = 0
        self.__right_canny__ = 0

        self.angle       = str
        self.left_angle  = str
        self.right_angle = str

        self.x_avr       = int

        self.x_center    = str

    def splitImg(self, data):
        self.__img__         = cv2.imdecode(np.frombuffer(data, np.uint8), 1)
        self.__img__         = self.__img__[300:, :]

        blur                 = cv2.GaussianBlur(self.__img__, (7,7),1.5, 1.5)

        self.__canny__       = cv2.Canny(blur, 50, 100)

        self.__left_canny__  = self.__canny__[:, :320]
        self.__right_canny__ = self.__canny__[:, 320:]

    def drawAngle(self):
        topPoint = self.__canny__[0:1, :]
        lowPoint = self.__canny__[199:200, :]

        left_top  = 0
        right_top = 0

        count_left_top  = 0
        count_right_top = 0

        for i in range(320):
            if topPoint[0, i] == 255:
                left_top += i
                count_left_top += 1

            if topPoint[0, i+320] == 255:
                right_top += i+320
                count_right_top += 1

        try:
            left_top  = left_top  / count_left_top
            right_top = right_top / count_right_top

            top = left_top + right_top / 2

            angle = (float)(top - 320) / (float)(200)

            cv2.line(self.__img__, (top, 0), (320, 320), (0,250,250), 3, cv2.CV_AA)

            self.angle = str(angle)

        except:
            self.angle = "error"

    def drawLine(self, lines, img, flag):
        try :
            a,b,c = lines.shape
        except :
            return 0, 0

        total_angle = 0
        total_x = 0
        count_line = 0

        for i in range(a):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0, y0 = a*rho, b*rho
            pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
            pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )

            x1, y1 = pt1 # point which component line
            x2, y2 = pt2

            x3 = x1 + x2
            x3 = x3 / 2 # find center x point of the line
            self.x_center = x3

            try:
                angle = (float)(x2 - x1) / (float)(y2 - y1)
            except:
                angle = 0

            total_angle += angle

            count_line += 1

            if flag == 0 :
                total_x += x3
                cv2.line(img, (pt1[0], pt1[1]), (pt2[0], pt2[1]), (0, 0, 255), 3, cv2.CV_AA)
                cv2.line(img, (x3, 100), (x3, 200), (255,0,0), 3, cv2.CV_AA)

            else :
                total_x += x3 + 320
                cv2.line(img, (pt1[0]+320, pt1[1]), (pt2[0]+320, pt2[1]), (0, 0, 255), 3, cv2.CV_AA)
                cv2.line(img, (x3+320, 100), (x3+320, 200), (255,0,0), 3, cv2.CV_AA)

        try :
            return str(total_angle / count_line), int(total_x / count_line)
        except :
            print "error"
            return "error", 0

    def setImgInfo(self):
        lines       = cv2.HoughLines(self.__canny__, 1, math.pi/180.0, 100, np.array([]), 0, 0)
        left_lines  = cv2.HoughLines(self.__left_canny__, 1, math.pi/180.0, 100, np.array([]), 0, 0)
        right_lines = cv2.HoughLines(self.__right_canny__, 1, math.pi/180.0, 100, np.array([]), 0, 0)

        angle,       self.x_avr      = self.drawLine(lines,       self.__img__, 0)
        self.left_angle,  x_left     = self.drawLine(left_lines,  self.__img__, 0)
        self.right_angle, x_right    = self.drawLine(right_lines, self.__img__, 1)

        self.drawAngle()

        cv2.line(self.__img__, (self.x_avr, 100), (self.x_avr, 200), (0,255,0), 3, cv2.CV_AA)

    def getImg(self):
        return self.__img__

    def getCanny(self):
        return self.__canny__

    def getCenter(self):
        return self.x_center
