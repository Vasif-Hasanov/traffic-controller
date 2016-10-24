#!/bin/bash
#export node0="bbb-bb19.local"

#$$$$  1  $$$$$  1  $$$$
#$$$$     $$$$$     $$$$
#   2  1  3   2  2  3
#$$$$     $$$$$     $$$$
#$$$$  0  $$$$$  0  $$$$
#$$$$     $$$$$     $$$$
#$$$$  1  $$$$$  1  $$$$
#$$$$     $$$$$     $$$$
#   2  0  3   2  3  3
#$$$$     $$$$$     $$$$
#$$$$  0  $$$$$  0  $$$$

export node0="192.168.0.110" #bbb-bb19.local
export n0="tcp:\/\/$node0"

export node1="192.168.0.108" #"bbb-9178.local"
export n1="tcp:\/\/$node1"

export node2="192.168.0.105" #"bbb-9cbd.local"
export n2="tcp:\/\/$node2"

export node3="192.168.0.100" #"bbb-266a.local"
export n3="tcp:\/\/$node3"

export IC0_ip="$n0:5000"
export IC1_ip="$n1:5010"
export IC2_ip="$n2:5020"
export IC3_ip="$n3:5030"

#node 0 with node 1 north and node 3 east as neighbors
export lightSensor_ip="$n0:7000"
export densitySensor_ip="$n0:7100"
export LightActuator_ip="$n0:7001"
export IC_densityPub_ip=$IC0_ip
export filename="bbb0.json"

sed -e s/r0/r0/g nodeTemp.json > $filename
sed s/lightSensor_port/$lightSensor_ip/g -i $filename
sed s/densitySensor_port/$densitySensor_ip/g -i $filename
sed s/LightActuator_port/$LightActuator_ip/g -i $filename
sed s/IC_densityPub_port/$IC_densityPub_ip/g -i $filename
sed s/\"NICendpoint\"/\"$IC1_ip\"/g -i $filename
sed s/\"EICendpoint\"/\"$IC3_ip\"/g -i $filename
sed s/\"WICendpoint\"//g -i $filename
sed s/\"SICendpoint\"//g -i $filename

#Temporary replacements
#sed 's/\"Endpoints\":.*$/\"Endpoints\": []/g' -i $filename

#node 1 with node 2 east and node 0 south as neighbors
export lightSensor_ip="$n1:7010"
export densitySensor_ip="$n1:7110"
export LightActuator_ip="$n1:7011"
export IC_densityPub_ip=$IC1_ip
export filename="bbb1.json"


sed -e s/r0/r1/g nodeTemp.json > $filename
sed s/lightSensor_port/$lightSensor_ip/g -i $filename
sed s/densitySensor_port/$densitySensor_ip/g -i $filename
sed s/LightActuator_port/$LightActuator_ip/g -i $filename
sed s/IC_densityPub_port/$IC_densityPub_ip/g -i $filename
sed s/\"NICendpoint\"//g -i $filename
sed s/\"EICendpoint\"/\"$IC2_ip\"/g -i $filename
sed s/\"WICendpoint\"//g -i $filename
sed s/\"SICendpoint\"/\"$IC0_ip\"/g -i $filename
#Temporary replacements
#sed 's/\"Endpoints\":.*$/\"Endpoints\": []/g' -i $filename

#node 2 with node 3 south and node 1 west as neighbors
export lightSensor_ip="$n2:7020"
export densitySensor_ip="$n2:7120"
export LightActuator_ip="$n2:7021"
export IC_densityPub_ip=$IC2_ip
export filename="bbb2.json"

sed -e s/r0/r2/g nodeTemp.json > $filename
sed s/lightSensor_port/$lightSensor_ip/g -i $filename
sed s/densitySensor_port/$densitySensor_ip/g -i $filename
sed s/LightActuator_port/$LightActuator_ip/g -i $filename
sed s/IC_densityPub_port/$IC_densityPub_ip/g -i $filename
sed s/\"NICendpoint\"//g -i $filename
sed s/\"EICendpoint\"//g -i $filename
sed s/\"WICendpoint\"/\"$IC1_ip\"/g -i $filename
sed s/\"SICendpoint\"/\"$IC3_ip\"/g -i $filename
#Temporary replacements
#sed 's/\"Endpoints\":.*$/\"Endpoints\": []/g' -i $filename

#node 3 with node 0 west and node 2 north as neighbors
export lightSensor_ip="$n3:7030"
export densitySensor_ip="$n3:7130"
export LightActuator_ip="$n3:7031"
export IC_densityPub_ip=$IC3_ip
export filename="bbb3.json"

sed -e s/r0/r3/g nodeTemp.json > $filename
sed s/lightSensor_port/$lightSensor_ip/g -i $filename
sed s/densitySensor_port/$densitySensor_ip/g -i $filename
sed s/LightActuator_port/$LightActuator_ip/g -i $filename
sed s/IC_densityPub_port/$IC_densityPub_ip/g -i $filename
sed s/\"NICendpoint\"/\"$IC2_ip\"/g -i $filename
sed s/\"EICendpoint\"//g -i $filename
sed s/\"WICendpoint\"/\"$IC0_ip\"/g -i $filename
sed s/\"SICendpoint\"//g -i $filename
#Temporary replacements
#sed 's/\"Endpoints\":.*$/\"Endpoints\": []/g' -i $filename
