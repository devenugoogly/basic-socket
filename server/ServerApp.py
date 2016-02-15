'''
Created on Feb 7, 2016

@author: Devandra
'''
from BasicSocketServer import BasicSocketServer

if __name__ == '__main__':
    server = BasicSocketServer('127.0.0.1',5000)
    server.start();