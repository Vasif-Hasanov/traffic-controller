from zcm import *
import json
import logging
logging.basicConfig(level = logging.DEBUG)

class IC(Component):
    """Intersection controllor Component"""
    def __init__(self):
        Component.__init__(self)
        self.register_subscriber_operation("subGameLight", self.subGameLight)
        self.register_subscriber_operation("subGameDensity", subGameDensity)

        self.GameLightState = {}
        self.LightState = {}
        self.Densities = {}

    def subGameLight(self, message):
        self.GameLightState = json.loads(message)
        logging.debug("@subGameLight IC:%s GameLightState:%s", self.name, self.GameLightState)

    def subGameDensity(self, message):
        self.Densities = json.loads(message)
        logging.debug("@subGameDensity IC:%s gameDensity:%s", self.name, self.Densities)
