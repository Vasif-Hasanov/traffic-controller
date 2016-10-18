from zcm import *
import json


class IFIC(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)

        self.register_timer_operation("pubGameLightState", self.pubGameLightState)
        self.register_timer_operation("pubGameDensity", self.pubGameDensity)
        self.IC = self.name[-1] #NodeId

    def pubGameLightState(self):
        LightState = send2Game(getLightState(self.IC))
        self.publisher("game_lightState_pub").send(json.dumps(LigLightState))

    def pubGameDensity(self):
        gameDensity = send2Game(getDensity(self.IC))
        self.publisher("game_density_pub").send(json.dumps(gameDensity))

    def send2Game(msg):
        response = 0
        sock.settimeout(1)
        msg_string = json.dumps(msg)
        #sock.sendto(data_string, ("localhost", 11000))
        sock.sendto(msg_string, ("192.168.0.111", 11000))
        try:
            response_str, srvr = sock.recvfrom(1024)
            #logging.info("@SEND response_str: %s", pprint.pformat(response_str))
            response = json.loads(response_str)

        except socket.timeout:
            response = ""
            logging.warning('Request timed out')
        return response

    def getLightState(IC):
        msg = {
        'Method': 'GETSTATE',
        'Object': {
                    'Name': 'NodeId',
                    'Type': 'PARAMETER',
                    'Value': IC,  #// should be 0 - 3 (for the selected ids)
                    'ValueType': 'System.UInt32'
                    }
        }
        logging.debug('@GETSTATE msg: %s', pprint.pformat(msg))
        return msg;

    def getDensities(IC):
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

    def setLightState_All(IC, state):
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
