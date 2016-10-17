from zcm import *
import socket
from random import randint
import logging
import pprint
import json
#logging.basicConfig(level=logging.INFO)

class simServer_Component(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)

        self.Density = [randint(0,2) for i in xrange(4)]
        self.register_server_operation("returnDensity",
        self.returnDensity)
        self.register_server_operation("setState", self.setState)

        self.register_timer_operation("pubState", self.pubState)
        self.register_timer_operation("pubDensity", self.pubDensity)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #initialize:
        self.state_str = '{"segment0":{"vehicle":"Red"},"segment1":{"vehicle":"Red"},"segment2":{"vehicle":"Red"},"segment3":{"vehicle":"Red"}}'

        self.State = json.loads(self.state_str)
        self.initialized = False


        logging.info("simServer ready")
        #self.State =  {u'segment0': {'pedestrian': 'Red', u'vehicle': 'Green'},                       u'segment1': {'pedestrian': 'Red', u'vehicle': 'Green'},                       u'segment2': {'pedestrian': 'Red', u'vehicle': 'Green'}, u'segment3': {'pedestrian': 'Red', u'vehicle': 'Green'}}

    def send(self, data_string):
        response = 0
        self.sock.settimeout(1) #need this in case of message loss
        self.sock.sendto(data_string, ("192.168.0.111",11000))
        logging.debug('@send, I: %s, msg: %s\n', self.name, pprint.pformat(data_string))
        try:
            response, srvr = self.sock.recvfrom(1024)
            logging.debug('@send, name:%s response: %s',self.name,  response )
        except socket.timeout:
            logging.debug('Request timed out')
        return response

    def setState(self, msg_string):
        logging.debug("@SETSTATE name:%s msg_string:%s", self.name, msg_string)
        self.State = json.loads(msg_string)
        logging.debug('@SETSTATE name:%s state:\n%s\n', self.name, pprint.pformat(self.State))

        data = {
                'Method': 'SETSTATE',
                'Object':
                            {
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': self.name[-1],  #// should be 0 - 3 (for the selected ids)
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
                                            'Value': self.State['segment0']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value':self.State['segment0']['pedestrian'] ,
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
                                            'Value': self.State['segment1']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value':self.State['segment1']['pedestrian'] ,
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
                                            'Value': self.State['segment2']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value':self.State['segment2']['pedestrian'] ,
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
                                            'Value': self.State['segment3']['vehicle'],
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value':self.State['segment3']['pedestrian'],
                                    		'ValueType': 'System.String'
                                    	    }
	                                    ]
                            }
                }
        logging.debug("@SETSTATE name: %s data:\n%s", self.name, pprint.pformat(data))

        data_string = json.dumps(data)
        response = self.send(data_string)
        logging.info("@SETSTATE name:%s response:%s", self.name, response)
        return "ACK"

    def pubState(self):
        logging.debug("publish state")
        self.getState()
        self.publisher("statePublisher").send(self.state_str)

    def getState(self):
        logging.debug('name: %s\n', self.name)
        data = {
                'Method': 'GETSTATE',
                'Object': {
                	       'Name': 'NodeId',
                           'Type': 'PARAMETER',
                           'Value': self.name[-1],  #// should be 0 - 3 (for the selected Intersection)
                           'ValueType': 'System.UInt32'
                           }
               }
        data_string = json.dumps(data)
        logging.debug("@GETSTATE %s before send", self.name)
        response = self.send(data_string)
        logging.debug("@GETSTATE name:%s, response:%s", self.name, response)
        logging.debug("@GETSTATE %s after send\n", self.name)
        if type(response) is str:
            if (type(json.loads(response)) is dict) and bool(json.loads(response)) :
                self.state_str = response
                self.initialized = True
        else:
            logging.debug("Server not on. old state: %s", self.state_str)
        #print "msgID: ", msgID
        #return self.state_str;

    def pubDensity(self):
        if not self.initialized:
            self.getState()
            if self.initialized:
                self.State = json.loads(self.state_str)
        else:
            logging.debug("publish Density")
            for index, item in enumerate(self.State):
                logging.info("@pubDensity item:%s index:%s", item, index)
                seg = int(item[-1])
                self.Density[seg] = self.getDensity(seg)

            self.publisher("densityPublisher").send(json.dumps(self.Density))

    def getDensity(self, seg):
        data = {
                'Method': 'GETDENSITY',
                'Object':{
                            'Name': 'NodeId',
                        	'Type': 'PARAMETER',
                        	'Value': int(self.name[-1]),  #// should be 0 - 3 (for the selected ids)
                        	'ValueType': 'System.UInt32',
                        	'Parameters':
                            [
                        	    {
                        		'Name': 'SegmentId',
                        		'Type': 'PARAMETER',
                        		'Value': seg,
                        		'ValueType': 'System.UInt32'
                        	    }
                            ]
                         }
                }
        data_string = json.dumps(data)
        logging.debug("@GETDENSITY %s before send", self.name)
        response = self.send(data_string)
        logging.debug("@GETDENSITY name:%s, segment: %s, response:%s, type:%s", self.name, seg, response, type(response))

        if type(response) is str:
            if (type(json.loads(response)) is int) :
                density = json.loads(response)
                return density
        else:
            print "\n\n----------------------------------------"
            logging.error("Server not on. old density: %s", self.Density[seg])
            print "\n\n----------------------------------------"

            return self.Density[seg]

    def returnDensity(self, data_string):
        i = int(json.loads(data_string))
        return json.dumps(self.Density[i])
