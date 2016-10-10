from zcm import *
import socket
import logging
import pprint
logging.basicConfig(level=logging.INFO)

class ServerComponent(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)

        self.register_server_operation("getState",
        self.getState)

        self.register_server_operation("getDensity",
        self.getDensity)

        self.register_server_operation("setState",
        self.setState)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def getState(self, data_string):
        response = self.send(data_string)
        return response

    def send(self, data_string):
        self.sock.settimeout(1) #need this in case of message loss
        self.sock.sendto(data_string, ("192.168.0.111",11000))
        #logging.debug('@send, I: %s, msg: %s\n', self.name, pprint.pformat(data_string))
        try:
            response, srvr = self.sock.recvfrom(1024)
            #logging.debug('@send, response: %s', response )
        except socket.timeout:
            logging.error('Request timed out')
            response =  0
        return response

    def getDensity(self, segment):
        data = {
                'Method': 'GETDENSITY',
                'Object':{
                            'Name': 'NodeId',
                        	'Type': 'PARAMETER',
                        	'Value': int(self.name),  #// should be 0 - 3 (for the selected ids)
                        	'ValueType': 'System.UInt32',
                        	'Parameters':
                            [
                        	    {
                        		'Name': 'SegmentId',
                        		'Type': 'PARAMETER',
                        		'Value': segment[-1],
                        		'ValueType': 'System.UInt32'
                        	    }
                            ]
                         }
                }
        data_string = json.dumps(data)
        logging.debug('@getDensity before send')
        response = self.send(data_string)
        logging.debug('@getDensity, after send\n')
        logging.debug('@getDensity name=%s, Seg=%s; density: %s', self.name, segment[-1], response)
        if type(response) not in (int, str):
            print "\n\n"

            logging.error(
"\n ------@GETDENSITY RECEIVED BAD MESSAGE-----:\n \
_____________________________________________\n \
%s, type:%s \n\n", response, type(response))

            density = int(self.getDensity(segment))
            return density;
        else:
            density = int(response)
            return density;
