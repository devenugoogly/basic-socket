'''
Created on Feb 8, 2016

@author: devandra.raju
'''
import time
from matplotlib.cbook import Null
from data import Message
from enum import Enum
from common import *

class MessageType(Enum):
    ping = 1
    join = 2
    leave = 3
    msg = 4
    list = 5

class MessageBuilder:
    sMsgMarkerStart = "["
    sMsgMarkerEnd = "]"
    sHeaderMarker = "!h!"
    sBodyMarker = "!b!"
    sSeparator = ','
    incompleteBuffer = None
    
    def encode(self, mtype, source, body, received):
        payload = body.strip()
        print(payload)
        millis = int(round(time.time() * 1000))
        sb = self.sHeaderMarker+str(mtype)+self.sSeparator+str(millis)+self.sSeparator
        if received is not None:
            sb= sb+received;
        sb=sb+self.sSeparator
        
        if source is not None:
            sb=sb+source.strip()
        sb=sb+self.sSeparator
        
        if not(payload):
            sb=sb+str(0)
            sb=sb+self.sBodyMarker
        else:
            length = "%03d" % (len(payload))
            sb=sb+str(length)
            sb=sb+self.sBodyMarker
            if payload is not None:
                sb+=payload
        
        msg = str(sb);
        
        newsb =self.sMsgMarkerStart
        length = len(msg)
        newsb=newsb+str(length)
        newsb=newsb+msg
        newsb=newsb+self.sMsgMarkerEnd
        
        return str(newsb);
    
    
    def reset(self):
        self.incompleteBuffer = None;

    def isComplete(self):
        return (self.incompleteBuffer == None)
    
    def decode(self, raw):
        if raw == None:
            return None
        
        rtn = []
        s = str(raw)
        if self.incompleteBuffer != None:
            s = self.incompleteBuffer + s;
        
        msgs = s.split(self.sMsgMarkerStart)
        
        for m in msgs:
            print(m)
            if len(m) == 0:
                continue
            
            if not(m.endswith(self.sMsgMarkerEnd)):
                self.incompleteBuffer = self.sMsgMarkerStart + m
                break
            else:
                self.incompleteBuffer = None
            
            print("--> m (size = " + str(len(m)) + "): " + m);
            
            hdr = m.split(self.sHeaderMarker)
            if len(hdr) != 2:
                print("Unexpected message format")
                return None
            
            size = int(hdr[0])
            t = hdr[1]
            bd = t.split(self.sBodyMarker)
            
            if len(bd)!= 2:
                print('Unexpected message format (2)')
                return None
            
            header = bd[0]
            body = bd[1]
            body = body[0:len(body)-1]
        
            hparts = header.split(',')
            if len(hparts)!=5:
                print('Unexpected message format')
                return None
            
            bo = Message()
            bo.setType(hparts[0])
            
            if len(hparts[1]) > 0:
                bo.setReceived(long(float(hparts[1])))
                
            bo.setSource(hparts[1])
            
            bodySize = int(hparts[4])
            if bodySize != len(body):
                print("Body does not match checksum")
                return None
            
            bo.setPayload(body)

            print("--> h: " + header);
            print("--> b: " + body);
            
            rtn.append(bo)
            
        return rtn  
    