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
logging.basicConfig(level=logging.INFO)


class Intersection_Component(Component):
    """docstring for Network_Component"""
    def __init__(self):
        print("initialize")
        Component.__init__(self)
        #queue parameters
        self.Qs = [randint(0,2) for i in xrange(4)] #[N E S W]
        self.neighbors = [0, 0, 0, 0]
        self.minInterval = [5, 5]#stay in state at least 20s
        self.maxInterval = [20, 20]#don't stay longer than 60s in state1/80s in state 2
        self.threshold1 = [20, 20] #if density % is lower don't switch
        self.threshold2 = [40, 40] #if density % if higher don't switch
        self.statesList = ['1', '2']
        self.currentIdx = 0
        self.clock = 0
        #pp.pprint(self.clock)
        #register timer
        self.State = {}
        self.ServerState = {}
        self.register_timer_operation("update", self.update)
        #register subscriber function
        self.register_subscriber_operation("coordinateQN", self.coordinateQN)
        self.register_subscriber_operation("coordinateQE", self.coordinateQE)
        self.register_subscriber_operation("coordinateQS", self.coordinateQS)
        self.register_subscriber_operation("coordinateQW", self.coordinateQW)
        self.register_subscriber_operation("subState", self.subState)
        self.register_subscriber_operation("subDensity", self.subDensity)
        #self.sensors = ['N', 'E', 'S', 'W']
        #pp.pprint(self.name) name hasn't been set yet...?
        #how do you call a function immediately after running __init__?
        self.initialized = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.bind((UDP_IP, UDP_PORT))
        self.msgID = 123

    def update(self):
        if (bool(self.ServerState) and not self.initialized):
            logging.info('@UPDATE First run I=%s\n', self.name)
            self.initialized = True
            self.State = self.ServerState
            #self.State = self.getState() #populate State, so we can set it.
            logging.info('@UPDATE: self.State: %s', self.State)
            for index, item in enumerate(self.State):
                logging.info("@UPDATE name:%s, index:%s, seg:%s", self.name, index, item)
                seg = int(item[-1])
                if seg in (0, 1):
                    self.State[item]['vehicle'] = 'Red'
                    self.State[item]['pedestrian'] = 'Red'
                    #self.setState(item, "Red", "Red")
                else:
                    self.State[item]['vehicle'] = 'Green'
                    self.State[item]['pedestrian'] = 'Red'
            self.setState()

            self.clock = time()
        elif (not self.initialized):
            logging.info("@UPDATE name: %s Waiting for server", self.name)
        else:
            if True == self.controllor():
                self.switchState()
                self.clock = time()
            else:
                self.keepState()
        '''
        #NEED SOME WAY TO FIGURE OUT WHO NEIGHBORS ARE
        NQ_data ={
                    'Intersection': int(self.name[-1]),
                    'Segment': "NQ",
                    'QDensity': self.Qs[0],
                    'State': self.statesList[self.currentIdx]
                }
        EQ_data ={
                    'Intersection': int(self.name[-1]),
                    'Segment': "EQ",
                    'QDensity': self.Qs[1],
                    'State': self.statesList[self.currentIdx]
                }
        WQ_data ={
                    'Intersection': int(self.name[-1]),
                    'Segment': "WQ",
                    'QDensity': self.Qs[2],
                    'State': self.statesList[self.currentIdx]
                }
        SQ_data ={
                    'Intersection': int(self.name[-1]),
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
        '''

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
                GreenQ += self.Qs[idx] + int(self.neighbors[idx]*.3)
            elif (self.State[i]['vehicle']) == 'Red':
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
        #self.State = self.getState()

      #The state has a min/max time and queue length for state. State is 1 or 2
        self.currentIdx = (self.currentIdx + 1) % len(self.statesList)
        #pp.pprint("@switchState - current state: ", self.State)
        #print self.State
        logging.debug("@SWITCHSTATE %s: currentState: \n %s\n", self.name, pprint.pformat(self.State))


        for index, item in enumerate(self.State):
            logging.debug('@SWITCHSTATE name:%s %s\n\n',self.name, item)
            if (self.State[item]['vehicle']) == 'Green':
                self.State[item]['vehicle'] = 'Red'
                self.State[item]['pedestrian'] = 'Red'
                #self.setState(i, "Red", "Red")
            elif (self.State[item]['vehicle']) == 'Red':
                self.State[item]['vehicle'] = 'Green'
                self.State[item]['pedestrian'] = 'Red'
                #self.setState(i, "Green", "Red")
            else:
                assert False
        self.setState()

        print "\n"
        logging.debug("@SWITCHSTATE--- %s---: NEW STATE: \n %s \n",self.name, pprint.pformat(self.State))


    def keepState(self):
        pass

    def coordinateQ(self, msg, segment):
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

    def coordinateQN(self, msg):
        self.coordinateQ(msg, "N")
    def coordinateQE(self, msg):
        self.coordinateQ(msg, "E")
    def coordinateQS(self, msg):
        self.coordinateQ(msg, "S")
    def coordinateQW(self, msg):
        self.coordinateQ(msg, "W")

    def subState(self, message):
        logging.debug("@subState: message recieved: %s", message)
        self.ServerState = json.loads(message)
        print "\n"
        logging.info('@SUBSTATE name:%s, serverState:\n %s', self.name, pprint.pformat(self.ServerState))
        print "\n"

    def subDensity(self, message):
        logging.debug("@subDensity: message recieved: %s", message)
        self.Qs = json.loads(message)

    def setState(self):
        logging.debug('@SETSTATE name:%s state:\n%s\n', self.name, pprint.pformat(self.State))

        msg_string = json.dumps(self.State)
        response = self.client("setState_port").call(msg_string)
        logging.info('name:%s response:%s', self.name, response)
