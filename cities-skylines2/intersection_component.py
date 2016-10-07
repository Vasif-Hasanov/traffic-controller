from zcm import *
from random import randint
import config
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
from time import time
import socket
import logging
logging.basicConfig(level=logging.DEBUG)


class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        print("initialize")
        Component.__init__(self)
        #queue parameters
        self.Qs = [randint(0,2) for i in xrange(4)] #[N E S W]
        self.neighbors = [0, 0, 0, 0]
        self.minInterval = [20, 20]#stay in state at least 20s
        self.maxInterval = [60, 80]#don't stay longer than 60s in state1/80s in state 2
        self.threshold1 = [20, 20] #if density % is lower don't switch
        self.threshold2 = [40, 40] #if density % if higher don't switch
        self.statesList = ['1', '2']
        self.currentIdx = 0
        self.clock = 0
        #pp.pprint(self.clock)
        #register timer
        self.State = {}
        self.register_timer_operation("update", self.update)
        #register subscriber function
        self.register_subscriber_operation("coordinateN", self.coordinateN)
        self.register_subscriber_operation("coordinateE", self.coordinateE)
        self.register_subscriber_operation("coordinateS", self.coordinateS)
        self.register_subscriber_operation("coordinateW", self.coordinateW)
        #self.sensors = ['N', 'E', 'S', 'W']
        #pp.pprint(self.name) name hasn't been set yet...?
        #how do you call a function immediately after running __init__?
        self.initialized = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.bind((UDP_IP, UDP_PORT))
        self.prefix = 'segment'

    def update(self):
        if not self.initialized:
            logging.info('@UPDATE First run I=%s\n', self.name)
            self.initialized = True
            self.switchState()
            self.clock = time()

        if True == self.controllor():
            self.switchState()
            self.clock = time()
        else:
            self.keepState()
            #self.clock += 1
        #self.simStep(self.statesList[self.currentIdx])

        #NEED SOME WAY TO FIGURE OUT WHO NEIGHBORS ARE
        NQ_data ={
                    'Intersection': int(self.name),
                    'Segment': "NQ",
                    'QDensity': self.Qs[0],
                    'State': self.statesList[self.currentIdx]
                }
        EQ_data ={
                    'Intersection': int(self.name),
                    'Segment': "EQ",
                    'QDensity': self.Qs[1],
                    'State': self.statesList[self.currentIdx]
                }
        WQ_data ={
                    'Intersection': int(self.name),
                    'Segment': "WQ",
                    'QDensity': self.Qs[2],
                    'State': self.statesList[self.currentIdx]
                }
        SQ_data ={
                    'Intersection': int(self.name),
                    'Segment': "SQ",
                    'QDensity': self.Qs[3],
                    'State': self.statesList[self.currentIdx]
                }

        NQ_data_string = json.dumps(NQ_data)
        EQ_data_string = json.dumps(EQ_data)
        SQ_data_string = json.dumps(SQ_data)
        WQ_data_string = json.dumps(WQ_data)

        self.publisher("pushNQ").send(NQ_data_string)
        self.publisher("pushEQ").send(EQ_data_string)
        self.publisher("pushSQ").send(SQ_data_string)
        self.publisher("pushWQ").send(WQ_data_string)
        #print "pushed"
        #print self.name

    def controllor(self):
        currentState = self.statesList[self.currentIdx]
        delT = time() - self.clock
        logging.info("@controllor %s: Time elapsed: %f", self.name, delT)

        if delT < self.minInterval[self.currentIdx]:
            return False

        if delT >= self.maxInterval[self.currentIdx]:
            return True

        #get queue data
        redQ = 0
        GreenQ = 0
        logging.debug('@controllor %s state:\n%s', self.name, self.State)
        for idx, i in enumerate(self.State):
            if (self.State[i]['vehicle']) == 'Green':
                self.Qs[idx] = self.getDensity(i)
                GreenQ += self.Qs[idx] + int(self.neighbors[idx]*.3)
            elif (self.State[i]['vehicle']) == 'Red':
                self.Qs[idx] = self.getDensity(i)
                redQ += self.Qs[idx] + int(self.neighbors[idx]*.3)
            else:
                assert False

        # for i in xrange(len(currentState)):
        #     if '2' == currentState[i]:
        #         redQ += self.Qs[i]
        #     elif '0' == currentState[i]:
        #         GreenQ += self.Qs[i]
        #     else:
        #         assert False

        if redQ <= self.threshold1[self.currentIdx]:
            #print "redQ", redQ
            return False

        if GreenQ > self.threshold2[self.currentIdx]:
            #print "GreenQ", GreenQ
            return False
        else: #q1 > threshold1 and q2 < threshold2
            #print "true"
            return True

    def switchState(self):
        logging.debug("SWITCHING STATE")
        self.State = self.getState()

      #The state has a min/max time and queue length for state. State is 1 or 2
        self.currentIdx = (self.currentIdx + 1) % len(self.statesList)
        #pp.pprint("@switchState - current state: ", self.State)
        #print self.State
        logging.debug("@SWITCHSTATE %s: currentState: \n %s\n", self.name, pprint.pformat(self.State))
        '''
        for i in self.State:
            logging.info('-----------@switchState %s\n\n', i)
            if (self.State[i]['vehicle']) == 'Green':
                self.setState(i, "Red", "Red")
            elif (self.State[i]['vehicle']) == 'Red':
                self.setState(i, "Green", "Red")
            else:
                assert False
        '''
        if (self.State[self.prefix+str(0)]['vehicle'] == 'Green'):
            self.setState(self.prefix+str(0), "Red", "Red")
            self.setState(self.prefix+str(3), "Red", "Red")
            self.setState(self.prefix+str(1), "Green", "Red")
            self.setState(self.prefix+str(2), "Green", "Red")

        else:
            self.setState(self.prefix+str(0), "Green", "Red")
            self.setState(self.prefix+str(3), "Green", "Red")
            self.setState(self.prefix+str(1), "Red", "Red")
            self.setState(self.prefix+str(2), "Red", "Red")
        ''''''
        logging.debug("@SWITCHSTATE %s: NEW STATE: \n %s \n",self.name, pprint.pformat(self.State))


    def keepState(self):
        pass

    # def simStep(self, currentState):
    #     for i in xrange(len(currentState)):
    #         if '2' == currentState[i]:
    #             self.Qs[i] += randint(0, 1)
    #         elif '0' == currentState[i]:
    #             self.Qs[i] += randint(-self.Qs[i], 1)
    #         else:
    #             assert False

    def coordinate(self, msg, segment):
        #segment is which port received the message
        #(compare states)
        data = json.loads(msg)
        if segment == "N":
            self.neighbors[0] = int(data['QDensity'])
        elif segment == "E":
            self.neighbors[1] = int(data['QDensity'])
        elif segment == "S":
            self.neighbors[2] = int(data['QDensity'])
        elif segment == "W":
            self.neighbors[3] = int(data['QDensity'])
        else:
            assert False
        #{State, Intersection, Segment, QDensity}
        pp.pprint(msg + segment)
        #print (self.neighbors)

    def coordinateN(self, msg):
        self.coordinate(msg, "N")
    def coordinateE(self, msg):
        self.coordinate(msg, "E")
    def coordinateS(self, msg):
        self.coordinate(msg, "S")
    def coordinateW(self, msg):
        self.coordinate(msg, "W")

        #print str(self.name) + " N segment received " + msg
        #pp.pprint(self.__dict__)
        #pp.pprint("message" + msg)

    def getState(self):
        logging.debug('@GETSTATE node: %s\n', self.name)
        data = {
                'Method': 'GETSTATE',
                'Object': {
                	       'Name': 'NodeId',
                           'Type': 'PARAMETER',
                           'Value': self.name,  #// should be 0 - 3 (for the selected Intersection)
                           'ValueType': 'System.UInt32'
                           }
               }
        data_string = json.dumps(data)
        logging.debug("@GETSTATE %s before send", self.name)
        response = self.send(data_string)
        logging.debug("@GETSTATE %s after send\n", self.name)
        #state = json.load(response)
        #with open('dummy.json') as node_string:
        state = json.loads(response)
        logging.debug("@GETSTATE: Response from simulator: \n %s\n", pprint.pformat(state))
        return state

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
	#pp.pprint(data_string)
        logging.debug('@getDensity before send')
        response = self.send(data_string)
        logging.debug('@getDensity, after send\n')
        logging.info('@getDensity\nIntscn=%s, Seg=%s; density: %s\n\n', self.name, segment[-1], response)
        #print response
	#density = int(json.loads(response))
        #density = randint(0, 100)
        density = int(response)
        return density;

    def setState(self, segment, vehicleState, pedestrianState ):
        self.State[segment]['vehicle'] = vehicleState
        self.State[segment]['pedestrian'] = pedestrianState
        logging.debug('@SETSTATE name:%s, seg:%s, state:\n%s', self.name, segment[-1], self.State)
        data = {
                'Method': 'SETSTATE',
                'Object':
                            {
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
                                            'ValueType': 'System.UInt32'	    },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': vehicleState,
                                            'ValueType': 'System.String'	    },
                                    	    {
                                    		'Name': 'PedestrianState',
                                    		'Type': 'PARAMETER',
                                    		'Value': 'Red',
                                    		'ValueType': 'System.String'
                                    	    }
	                                    ]
                            }
                }
        data_string = json.dumps(data)
	#print data_string
        logging.debug('@SETSTATE %s before send\n', segment[-1])
        response = self.send(data_string)
        logging.debug('@SETSTATE, after send\n')
	#print response
        #response = "ACK"
        return response

    def send(self, data_string):
        self.sock.settimeout(1) #need this in case of message loss
        self.sock.sendto(data_string, ("192.168.0.111",11000))
        logging.debug('@send, I: %s, msg: %s\n', self.name, pprint.pformat(data_string))
        try:
            response, srvr = self.sock.recvfrom(1024)
            logging.debug('@send, response: %s', response )
        except socket.timeout:
            logging.ERROR('Request timed out')
            response =  {u'segment0': {u'vehicle': u'Red'},
                         u'segment1': {u'vehicle': u'Red'},
                         u'segment2': {u'vehicle': u'Red'},
                         u'segment3': {u'vehicle': u'Red'}}
        return response
