import os
import time
from sendsms import sms

FNAME = './sms/manager/phone_book'
MSG = '모방 자율 주행 모드를 시작합니다.'

class Manager(object):
    def __init__(self, ID, pw, sender):
        self.identity   = ID
        self.password   = pw
        self.sender     = sender
        self.receiver   = list()
        self.issent     = False

        self.sms = sms()

    def getFileInfo(self):
        file_reader = open(FNAME, "r")
        self.receiver = file_reader.readlines()

    def sendSMS(self):
        self.getFileInfo()
        for who in self.receiver:
            self.sms.sms(self.identity, self.password, self.sender, who, time.ctime() + MSG)
