'''
Created on Feb 7, 2016

@author: Devandra
'''
import sys
import socket               # Import socket module
import threading
from common import *

class BasicSocketServer:
    connections = []
    forever = True
    idCounter = 1
    def __init__( self, host='127.0.0.1', port=2222):
        self.sd = socket.socket()
        self.host = host 
        self.port = port               
        
    def start(self):
        self.sd.bind((self.host, self.port))
        print("Host:",self.host,"Port:",self.port)      
        self.sd.listen(5)
        self.monitor = BasicSocketServer.MonitorSessions(30 * 1000 * 60,60 * 1000 * 60)
        while self.forever:
            c, addr = self.sd.accept()
            if not(self.forever):
                break;

            print("--> server got a client connection");
            self.idCounter = self.idCounter+1
            sh = BasicSocketServer.SessionHandler(c, self.idCounter);
            self.connections.append(sh);
            sh.start();
     
    class SessionHandler(threading.Thread):
    
        timeout = 10 * 1000
        forever = True
        def __init__(self,connection,Id):
            threading.Thread.__init__(self)
            self.connection = connection
            self.Id = Id

        def send(self, msg):
            for sh in BasicSocketServer.connections:
                print(sh.getSessionName())
        
        def sendTo(self, to, msg):
            for sh in BasicSocketServer.connections:
                if sh.getSessionName().tolower() in to:
                    break;
             
        def removeSession(self):
            BasicSocketServer.connections.remove();
            
        def stopSession(self):
            self.forever = False;
            if self.connection != None:
                self.removeSession()
                self.connection.close();
            self.connection = None;
            
        def getSessionId(self):
            return self.Id;
        
        def getLastContact(self):
            return self.lastContact
        
        def setTimeOut(self, v):
                self.timeout = v;
        
        def setSessionName(self, n):
                self.name = n;
        
        def getSessionName(self):
                return self.name;
            
        def run(self):
            print("Session " + str(self.Id) + " started");
            self.connection.settimeout(self.timeout);
            builder = MessageBuilder();
            while (self.forever):
                raw = self.connection.recv(1024)
                lenght = len(raw);
                if (lenght == 0):
                    continue;
                elif (lenght == -1):
                    break;
                            
                ls = builder.decode(raw);
                for msg in ls:
                    if (msg.getType() == MessageType.leave):
                        return;
                    elif (msg.getType() == MessageType.join):
                        print("--> join: "+ msg.getSource());
                    elif (msg.getType() == MessageType.msg):
                        print("--> msg: "+ msg.getPayload());
        
                self.lastContact = time.time()*1000;
        
    class MonitorSessions(threading.Thread):
        forever = True;
        interval = 0;
        idleTime=0;

        def __init__(self,interval,idleness):
            threading.Thread.__init__(self)
            self.interval = interval;
            self.idleTime = idleness;
    
        def stopMonitoring(self):
            self.forever = False;
    
        def run(self):
            while (self.forever):
                idle = time.time()*1000 - self.idleTime;
                time.sleep(self.interval);
                if (not(self.forever)):
                    break;
    
                for sh in self.connections:
                    if (sh.getLastContact() < idle):
                        print("MonitorSessions stopping session "+ sh.getSessionId());
                        sh.stopSession();
                        self.connections.remove(sh);
            
               