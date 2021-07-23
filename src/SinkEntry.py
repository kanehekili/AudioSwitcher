'''
Created on 16 Jul 2021

@author: matze
'''

class Sink(object):
    '''
    Data of a pulseaudio sink
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.data={}
        
    def setIndex(self,line):
        #parse sth like: index: 4
        idx = line.split(':')[1].strip()
        self.data["index"]=idx
        
    def index(self):
        self.data.get("index","-1")
        
    def setCard(self,line):
        card = line.split(':')[1].strip()
        #todo rm <>
        self.data["name"]=card
        
    def cardName(self):
        self.data().get("name","?")
    
    def setState(self,line):
        res = line.split(':')[1].strip()
        self.data["state"]=res
    
    def state(self):
        self.data().get("state","?")