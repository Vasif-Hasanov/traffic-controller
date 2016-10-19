from zcm import *
import json
import pprint
import logging
from time import time
logging.basicConfig(level = logging.DEBUG)
import csv
import os.path

class IC(Component):
    """Intersection controllor Component"""
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("update", self.update)
        #self.register_timer_operation("control")

        self.register_subscriber_operation("subGameLight", self.subGameLight)
        self.register_subscriber_operation("subGameDensity", self.subGameDensity)

        self.register_subscriber_operation("subNIC", self.subNIC)
        self.register_subscriber_operation("subEIC", self.subEIC)
        self.register_subscriber_operation("subSIC", self.subSIC)
        self.register_subscriber_operation("subWIC", self.subWIC)

        self.GameLightState = {}
        self.LightState = {}
        self.Densities = {}
        self.initialized = False
        self.clock = time()
        self.minTime = 5
        self.maxTime = 20
        self.minDensity = 10
        self.maxDensity = 50
        self.cardDict = {'N':'segment1',
                         'E':'segment3',
                         'S':'segment0',
                         'W':'segment2'}
        self.SegDict = {'segment1':'N',
                        'segment3':'E',
                        'segment0':'S',
                        'segment2':'W'}
        self.ICs = {'NIC':0,
                    'EIC':0,
                    'SIC':0,
                    'WIC':0}
        self.weight = .3 #how much influence surrounding ICs have

    def update(self):
        #initialize the game light state
        if(bool(self.GameLightState)and not self.initialized):
            logging.info('@UPDATE initialize: %s', self.name)
            self.initialized = True
            self.LightState = self.GameLightState
            for seg in self.LightState:
                if self.SegDict[seg] in ('N', 'S'):
                    self.LightState[seg]['vehicle']='Green'
                    self.LightState[seg]['pedestrian']='Red'
                else:
                    self.LightState[seg]['vehicle']='Red'
                    self.LightState[seg]['pedestrian']='Red'
            self.setGameLights()
            self.clock = time()
        elif(not self.initialized):
            logging.info("@UPDATE name: %s Waiting for server", self.name)
        else:
            if True == self.controllor():
                self.switchState()
                self.clock = time()
            else:
                pass

    def controllor(self):
        dT = time() - self.clock
        if dT >= self.maxTime:
            return True

        if dT < self.minTime:
            return False
        RedQ = 0
        GreenQ = 0
        for seg in self.LightState:
            ICDs = self.ICs[self.SegDict[seg]+'IC']
            #print "----------{}------------".format(ICDs)
            if(self.LightState[seg]['vehicle'])=='Green':
                GreenQ += self.Densities[seg] + ICDs*self.weight
            else:
                RedQ += self.Densities[seg] + ICDs*self.weight

        #print "name:{}, redQ:{}".format(self.name, RedQ)
        #print "name:{}, GreenQ:{}".format(self.name, GreenQ)
        if RedQ <= self.minDensity:
            return False
        if GreenQ > self.maxDensity:
            return False
        else:
            return True

    def subNIC(self, msg_str):
        msg = json.loads(msg_str)
        IC = msg['Densities']
        segA = IC[self.cardDict['N']]
        segB = IC[self.cardDict['E']]
        segC = IC[self.cardDict['W']]
        self.ICs['NIC'] = segA + segB + segC
        logging.debug("@subNIC IC:%s NIC:\n%s\n",self.name, pprint.pformat(self.ICs['NIC']))
    def subEIC(self, msg_str):
        msg = json.loads(msg_str)
        IC = msg['Densities']
        segA = IC[self.cardDict['N']]
        segB = IC[self.cardDict['E']]
        segC = IC[self.cardDict['S']]
        self.ICs['EIC'] = segA + segB + segC
        logging.debug("@subEIC IC:%s EIC:\n%s\n", self.name, pprint.pformat(self.ICs['EIC']))
    def subSIC(self, msg_str):
        msg = json.loads(msg_str)
        IC = msg['Densities']
        segA = IC[self.cardDict['E']]
        segB = IC[self.cardDict['S']]
        segC = IC[self.cardDict['W']]
        self.ICs['SIC'] = segA + segB + segC
    def subWIC(self, msg_str):
        msg = json.loads(msg_str)
        IC = msg['Densities']
        segA = IC[self.cardDict['N']]
        segB = IC[self.cardDict['S']]
        segC = IC[self.cardDict['W']]
        self.ICs['WIC'] = segA + segB + segC
    def switchState(self):
        for seg in self.LightState:
            if(self.LightState[seg]['vehicle'])=='Green':
                self.LightState[seg]['vehicle']='Red'
                self.LightState[seg]['pedestrian']='Red'
            else:
                self.LightState[seg]['vehicle']='Green'
                self.LightState[seg]['pedestrian']='Red'
        self.setGameLights()

    def subGameLight(self, message):
        self.GameLightState = json.loads(message)
        logging.debug("@subGameLight IC:%s \nGameLightState:\n%s\n", self.name, pprint.pformat(self.GameLightState))

    def subGameDensity(self, message):
        self.Densities = json.loads(message)
        logging.debug("@subGameDensity IC:%s gameDensity:%s\n", self.name, self.Densities)

        file_exists=os.path.isfile(self.name+".csv")
        with open(self.name+".csv", 'ab') as csvfile:
            fieldnames = self.cardDict.values()
            dW = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                dW.writeheader()
            dW.writerow(self.Densities)
            print "write to file"
            #csvfile.flush()

        ICD = {'IC': self.name,
               'Densities' : self.Densities}
        ICD_str = json.dumps(ICD)
        self.publisher("density_pub").send(ICD_str)

    def setGameLights(self):
        msg_string = json.dumps(self.LightState)
        response = self.client("setGameLightState_client").call(msg_string)
        logging.debug("@setGameLights IC:%s success:%s", self.name, json.loads(response))


    #$$$$  1  $$$$$  1  $$$$
    #$$$$     $$$$$     $$$$
    #   2  1  3   2  2  3
    #$$$$     $$$$$     $$$$
    #$$$$  0  $$$$$  0  $$$$
    #$$$$     $$$$$     $$$$
    #$$$$  1  $$$$$  1  $$$$
    #$$$$     $$$$$     $$$$
    #   2  0  3   2  3  3
    #$$$$     $$$$$     $$$$
    #$$$$  0  $$$$$  0  $$$$
