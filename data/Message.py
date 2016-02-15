'''
Created on Feb 10, 2016

@author: devandra.raju
'''
class Message:
    def getType(self):
        return self.messageType

    def setType(self,messageType):
        self.messageType = messageType

    def getSource(self):
        return self.source

    def setSource(self,source):
        self.source = source

    def getReceived(self):
        return self.received

    def setReceived(self,received):
        self.received = received

    def getPayload(self):
        return self.payload

    def setPayload(self,body):
        self.payload = body
    