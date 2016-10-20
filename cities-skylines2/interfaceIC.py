from zcm import *
import json
import logging
import socket
import pprint


class IFIC(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gameServerIP = "192.168.0.111"

        self.register_timer_operation("pubGameLightState", self.pubGameLightState)
        self.register_timer_operation("pubGameDensity", self.pubGameDensity)

        self.register_server_operation("setGameLightState", self.setGameLightState)

    def pubGameLightState(self):
        IC = self.name[-1]
        lightState = self.send2Game(self.getLightState(IC))
        self.publisher("game_lightState_pub").send(json.dumps(lightState))

    def pubGameDensity(self):
        IC = self.name[-1]
        gameDensity = self.send2Game(self.getDensities(IC))
        self.publisher("game_density_pub").send(json.dumps(gameDensity))

    def setGameLightState(self, msg_string):
        IC = self.name[-1]
        state = json.loads(msg_string)
        rep = self.send2Game(self.setLightState_All(IC, state))
        return json.dumps(rep)

    def send2Game(self, msg):
        response = 0
        self.sock.settimeout(1)
        msg_string = json.dumps(msg)
        #sock.sendto(data_string, ("localhost", 11000))
        self.sock.sendto(msg_string, (self.gameServerIP, 11000))
        try:
            response_str, srvr = self.sock.recvfrom(1024)
            #logging.info("@SEND response_str: %s", pprint.pformat(response_str))
            response = json.loads(response_str)

        except socket.timeout:
            response = ""
            logging.warning('Request timed out')
        return response

    def getLightState(self, IC):
        msg = {
        'Method': 'GETSTATE',
        'Object': {
                    'Name': 'NodeId',
                    'Type': 'PARAMETER',
                    'Value': IC,  #// should be 0 - 3 (for the selected ids)
                    'ValueType': 'System.UInt32'
                    }
        }
        return msg;

    def getDensities(self, IC):
        msg = {
                'Method': 'GETDENSITIES',
                'Object':{
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': IC,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                            [
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 0,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 1,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 2,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 3,
                                'ValueType': 'System.UInt32'
                                },

                            ]
                         }
                }
        return msg;

    def setLightState_All(self, IC, state):
        msg = {
                'Method': 'SETSTATE',
                'Object':
                            {
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': IC,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                                        [
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '0',
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment0']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment0']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '1',
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment1']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment1']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '2',
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment2']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment2']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '3',
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment3']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment3']['pedestrian'],
                                            'ValueType': 'System.String'
                                            }
                                        ]
                            }
                }
        return msg
