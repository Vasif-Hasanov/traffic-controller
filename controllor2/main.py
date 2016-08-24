import config
import intersection
import subprocess
import os
import time
import traci

if __name__ == '__main__':
    name = '1443088101'
    test = intersection.Intersection(name)
    test.loadFromDict(config.data)
    sumoMap = os.path.join('..','VanderbiltCampus','Vanderbilt.sumo.cfg')
    port = 11111
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", sumoMap, "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)
    time.sleep(10)
    traci.init(port)
    time.sleep(10)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        test.run()
