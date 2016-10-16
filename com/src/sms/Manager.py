import os
from sendsms import sms

FNAME = './manager/phone_book'

class Manager(object):
    def __init__(self, ID, pw, sender):
        self.identity   = ID
        self.password   = pw
        self.sender     = sender
        self.receiver   = list()

        self.sms = sms()

    def getFileInfo():
        file_reader = open(FNAME, "r")
        self.receiver = file_reader.readlines()

    def sendSMS():
        getFileInfo()
        for who in self.receiver:
            sms(self.identity, self.password, self.sender, who)
