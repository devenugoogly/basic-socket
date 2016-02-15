'''
Created on Feb 7, 2016

@author: Devandra
'''
import socket
from common.MessageBuilder import *

class BasicClient:
    def __init__(self,host='127.0.0.1',port=5000):
        self.host = host
        self.port = port
        self.sd = socket.socket()
    
    def setName(self,name):
        self.name = name

    def getName(self):
        return self.name
    
    def startSession(self):
        self.sd.connect((self.host,self.port))
        print("Connected to Host:",self.host,"@ Port:",self.port)

    def stopSession(self):
        builder = MessageBuilder()
        msg = builder.encode(MessageType.leave, self.name,'', '')
        print(msg)
        self.sd.send(msg)
        self.sd.close()
        self.sd = None
    
    def join(self,name):
        builder = MessageBuilder()
        self.name = name
        msg = builder.encode(MessageType.join, name, '', '')
        self.sd.send(msg)
        
    def sendMessage(self,message):
        if len(message) > 1024:
            print('message exceeds 1024 size')
            
        builder = MessageBuilder()
        msg = builder.encode(MessageType.msg,self.name,message,'')
        self.sd.send(msg)
