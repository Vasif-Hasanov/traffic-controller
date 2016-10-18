from zcm import *
import json
import pprint
import logging
from time import time
logging.basicConfig(level = logging.DEBUG)

class IC(Component):
    """Intersection controllor Component"""
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("update", self.update)
        #self.register_timer_operation("control")

        self.register_subscriber_operation("subGameLight", self.subGameLight)
        self.register_subscriber_operation("subGameDensity", self.subGameDensity)

        self.GameLightState = {}
        self.LightState = {}
        self.Densities = {}
        self.initialized = False
        self.clock = time()
        self.minTime = 5
        self.maxTime = 20
        self.cardDict = {'N':'segment1',
                         'E':'segment3',
                         'S':'segment0',
                         'W':'segment2'}
        self.SegDict = {'segment1':'N',
                        'segment3':'E',
                        'segment0':'S',
                        'segment2':'W'}

    def update(self):
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


    def subGameLight(self, message):
        self.GameLightState = json.loads(message)
        logging.debug("@subGameLight IC:%s \nGameLightState:\n%s\n", self.name, pprint.pformat(self.GameLightState))

    def subGameDensity(self, message):
        self.Densities = json.loads(message)
        logging.debug("@subGameDensity IC:%s gameDensity:%s\n", self.name, self.Densities)

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
