'''
Created on Dec 21, 2019

@author: matze
'''
import subprocess
from subprocess import Popen
import re
class PulseAudioControl():
    PA_CTL="/usr/bin/pactl"
    #PA_CMD="/usr/bin/pacmd"
    ISPROFILE = re.compile('Profiles:')
    ISPORT = re.compile('Ports:')
    ACTIVE_PROFILE=re.compile('Active Profile: output:([A-z:-]+)+')
    PROFILE=re.compile("output:([0-9A-z:-]+)+: ([\S ]+)+available:([ A-z]+)" )
    KEY_LOCAL="analog"
    KEY_EXTERN="hdmi"
    def __init__(self):
        #pactl set-card-profile 0 output:analog-stereo
        #pactl set-card-profile 0 output:hdmi-stereo
        self.profilList=[]
        self.activeProfile=None
        self.lastError=None
        self.readCards()
         
     
    def readCards(self):
        cmd =[self.PA_CTL,"list","cards"]
        result = Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        if len(result[1])>0:
            self.lastError=result[1]
            return
        cardData = result[0].decode("utf-8")
        self._parseData(cardData)
        self.lastError=None       
    
    def switchProfile(self,type):
        cmd=[self.PA_CTL,"set-card-profile","0","output:"+type]
        result = Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        if len(result[1])>0:
            self.lastError=result[1]
            return
        self.lastError=None
    
    def _parseData(self,cardData):
        inProfile=False
        
        for line in cardData.splitlines():
            line = line.strip()
            if self.ISPROFILE.match(line):
                inProfile=True
                continue
            if self.activeProfile is None:
                active = self.ACTIVE_PROFILE.search(line)
                if active:
                    inProfile=False
                    #print("active profile:",active.group(1))
                    self.activeProfile = active.group(1)
                
            if self.ISPORT.match(line):
                break;
            
            if inProfile:  
                m= self.PROFILE.search(line)
                if m:
                    dev=m.group(1)
                    desc = m.group(3).strip()
                    #print ("profile dev:%s descr:%s"%(dev,desc))
                    if desc[0]!= 'n':
                        self.profilList.append(dev)     
     
    def currentProfile(self):
        return self.activeProfile
     
    def validProfiles(self):
        return self.profilList
    
    def getPrimaryLocalProfile(self):
        for profile in self.profilList:
            if self.KEY_LOCAL in profile:
                return profile
        return self.profilList[0]
    
    def getPrimaryExternalProfile(self):
        for profile in self.profilList:
            if self.KEY_EXTERN in profile:
                return profile
        return None
    
    def isLocalProfile(self):
        return self.activeProfile == self.getPrimaryLocalProfile()
                    
     
    def printState(self):
        print("Current profile: ",self.activeProfile)
        for profile in self.profilList:
            print(">",profile) 
        
        print("Local %s  Extern: %s"%(self.getPrimaryLocalProfile(),self.getPrimaryExternalProfile()))
        print ("is Local:",self.isLocalProfile() )


class PaCmd():
    PA_SINKS=["/usr/bin/pacmd","list-sinks"]
    PA_IN=["/usr/bin/pacmd","list-sink-inputs"]
    def __init__(self):
        sinks=[]
        self.lastError=None
        
    def readSinks(self):
        result = Popen(self.PA_SINKS,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        if len(result[1])>0:
            self.lastError=result[1]
            return
        cardData = result[0].decode("utf-8")
        self._parseSinks(cardData)
        self.lastError=None       
                  
    def _parseSinks(self,data):
        for line in data.splitlines():
            tabcnt = line.count('\t')
            print(line,">>",tabcnt)              

    def readInputs(self):           
        result = Popen(self.PA_IN,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        if len(result[1])>0:
            self.lastError=result[1]
            return
        cardData = result[0].decode("utf-8")
        self._parseInputSinks(cardData)
        self.lastError=None       
                 
    def _parseInputSinks(self,data):
        for line in data.splitlines():
            tabcnt = line.count('\t')
            print(line,">>",tabcnt) 
            print(line)                  
                
def parseTest():
    ISPROFILE = re.compile('profiles:')
    ACTIVE_PROFILE=re.compile('Active Profile: output:([A-z:-]+)+')
    PROFILE=re.compile("output:([0-9A-z:-]+)+: ([\S ]+)+available:([ A-z]+)" )
    txt2 = 'output:analog-stereo: Analog Stereo Output (sinks: 1, sources: 0, priority: 6500, available: yes'
    txt3 = "Active Profile: output:analog-stereo"
    txt4 = 'profiles:'
    if ISPROFILE.match(txt4):
        print("Profile_ID")
    m=ACTIVE_PROFILE.search(txt3)
    if m is not None:
        print("active:",m.group(0))
        for item in m.groups():
            print("1:%s"%(item))
    m=PROFILE.search(txt2)    
    print("profile:",m.group(0))
    for item in m.groups():
        print("1:%s"%(item))    

def testControl():
    test = PulseAudioControl()
    #Error if no external profile available!
    test.printState()
    extProfile=test.getPrimaryExternalProfile()
    if test.isLocalProfile() and extProfile:
        test.switchProfile(extProfile)
    else:
        test.switchProfile(test.getPrimaryLocalProfile())
    parseTest()

def regTst():
    t1 = "   index: 1"
    t2 = "/tstate: RUNNING"
    t3="sink: 4 <alsa_output.pci-0000_00_1b.0.analog-stereo>"
    t4="properties:" #then key value pairs
    #list-sinks..
    t5="  * index: 4"
    t6="/tname: <alsa_output.pci-0000_00_1b.0.analog-stereo>"
    t7="/tstate: IDLE"
     
def testCmd():
    x=PaCmd()
    x.readInputs()
    x.readSinks()
     
if __name__ == '__main__':
    #testControl()
    testCmd()
    pass