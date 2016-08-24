import sys
sys.path.append("/home/local/VANDERBILT/liy29/sumo-0.24.0/tools/")
import traci


class State(object):
    def __init__(self, _state, _phase, _min_interval, _max_interval, _threshold1, _threshold2):
        self.stateRow = _state
        self.phase = _phase
        self.minInterval = _min_interval
        self.maxInterval = _max_interval
        self.threshold1 = _threshold1
        self.threshold2 = _threshold2


class Intersection(object):
    def __init__(self, _name):
        self.name = _name
        self.statesList = []
        self.sensors = None
        self.clock = 0
        self.currentIdx = 0

    def loadFromDict(self, _dict):
        data = _dict[self.name]
        #TODO: check the correctness of input.
        self.sensors = data['sensors']
        stateMatrix = data['stateMatrix']
        for idx in range(len(stateMatrix)):
            stateRow = stateMatrix[idx]
            phase = data['stateToPhase'][stateRow]
            min_interval = data['minInterval'][idx]
            max_interval = data['maxInterval'][idx]
            threshold1 = data['threshold1'][idx]
            threshold2 = data['threshold2'][idx]
            state = State(stateRow, phase, min_interval, max_interval, threshold1, threshold2)
            self.statesList.append(state)

    def run(self):
        if True == self.controllor():
            self.switchState()
            self.clock = 0
        else:
            self.keepState()
            self.clock += 1

    def controllor(self):
        currentState = self.currentState()
        if self.clock < currentState.minInterval:
            return False

        if self.clock >= currentState.maxInterval:
            return True

        qLength1, qLength2 = self.updateQueueLength()

        if qLength1 <= currentState.threshold1:
            return False

        if qLength2 > currentState.threshold2:
            return False
        else: #q1 > threshold1 and q2 < threshold2
            return True

    def keepState(self):
        traci.trafficlights.setRedYellowGreenState(self.name, self.statesList[self.currentIdx].phase)

    def switchState(self):
        self.currentIdx = (self.currentIdx + 1) % len(self.statesList)
        traci.trafficlights.setRedYellowGreenState(self.name, self.statesList[self.currentIdx].phase)

    def updateQueueLength(self):
        stateRow = self.currentState().stateRow
        q1 = 0
        q2 = 0
        for idx in range(len(stateRow)):
            sensor = self.sensors[idx]
            if '0' == stateRow[idx]:
                q1 += traci.areal.getLastStepVehicleNumber(sensor)
            elif '1' == stateRow[idx]:
                q2 += traci.areal.getLastStepVehicleNumber(sensor)
            else:
                assert False #should not reach here

        return q1, q2

    def currentState(self):
        return self.statesList[self.currentIdx]




