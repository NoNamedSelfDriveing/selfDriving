import os
from sendsms import sms

FNAME = './sms/manager/phone_book'
MSG = 'Changed itself'

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
            self.sms.sms(self.identity, self.password, self.sender, who, MSG)

if __name__ == "__main__":
    print 'start'
    sms = Manager("nonamed123", "nonamed123", "01047230479")
    sms.sendSMS()
