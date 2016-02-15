'''
Created on Feb 15, 2016

@author: devandra.raju
'''

import pickle

class PickelBuilder:
    def encode(self, data):
        ret = pickle.dumps(data)
        return ret

    def decode(self, data):
        ret = pickle.loads(data)
        return ret
