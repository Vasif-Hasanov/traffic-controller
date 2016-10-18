#!/bin/bash
#export node0="bbb-bb19.local"
export node0="192.168.0.110" #bbb-bb19.local
export n0="tcp:\/\/$node0"

export node1="bbb-9178.local"
export n1="tcp:\/\/$node1"

export node2="bbb-9cbd.local"
export n2="tcp:\/\/$node2"

export node3="bbb-266a.local"
export n3="tcp:\/\/$node3"


#node 0 with node 1 north and node 3 east as neighbors
export lightSensor_ip="$n0:7000"
export densitySensor_ip="$n0:7100"
export LightActuator_ip="$n0:7001"
export IC_densityPub_ip="$n0:5000"
sed -e s/lightSensor_port/$lightSensor_ip/g nodeTemp.json > bbb0.json

sed s/densitySensor_port/$densitySensor_ip/g -i bbb0.json
sed s/LightActuator_port/$LightActuator_ip/g -i bbb0.json
sed s/IC_densityPub_port/$IC_densityPub_ip/g -i bbb0.json

#Temporary replacements
sed 's/\"Endpoints\":.*$/\"Endpoints\": []/g' -i bbb0.json
