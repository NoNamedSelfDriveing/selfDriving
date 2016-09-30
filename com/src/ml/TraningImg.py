#-*- coding: utf-8 -*-

import cv2
import sys
import os
import numpy as np

y_dataset = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
# 직진 직좌 직우 정차

def makeTraningSet(imgcation, labelcation):
    x = []
    y = []

    imageList = os.listdir(imgcation)
    labelList = open(labelcation, 'r')

    for imageCount in range(len(imageList)):
        tmp = int(labelList.readline()[0])

        label = 0

        if tmp == 1:
            label = 0
        elif tmp == 5:
            label = 1
        elif tmp == 9:
            label = 2


        image = imgcation + '/' + imageList[imageCount]
        feed = readimage(image)
        x.append(feed)
        y.append(y_dataset[label])

    print 'finish read images'
    return x, y

def readimage(path):
    img = cv2.imread(path)

    data = cv2.resize(img, (28, 28))


    return data
