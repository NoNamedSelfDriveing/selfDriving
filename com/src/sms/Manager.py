import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sendsms import sms

FNAME = './sms/manager/phone_book'
MSG = "Status error detected, Changed Driving Mode"

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
        print 'sms sended'
        self.getFileInfo()
        for who in self.receiver:
            self.sms.sms(self.identity, self.password, self.sender, who, MSG)
