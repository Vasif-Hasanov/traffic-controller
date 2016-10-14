#!/bin/bash
export node0="bbb-bb19.local"
export n0="tcp:\/\/$node0:5000"
export e0="tcp:\/\/$node0:5001"
export s0="tcp:\/\/$node0:5002"
export w0="tcp:\/\/$node0:5003"

export node1="bbb-9178.local"
export n1="tcp:\/\/$node1:5010"
export e1="tcp:\/\/$node1:5011"
export s1="tcp:\/\/$node1:5012"
export w1="tcp:\/\/$node1:5013"

export node2="bbb-9cbd.local"
export n2="tcp:\/\/$node2:5020"
export e2="tcp:\/\/$node2:5021"
export s2="tcp:\/\/$node2:5022"
export w2="tcp:\/\/$node2:5023"

export node3="bbb-266a.local"
export n3="tcp:\/\/$node3:5030"
export e3="tcp:\/\/$node3:5031"
export s3="tcp:\/\/$node3:5032"
export w3="tcp:\/\/$node3:5033"

#node 0 with node 1 north and node 3 east as neighbors
sed -e s/Q1endpoints/$n1\",\"$e1\",\"$w1/g nodeTemp.json > bbb0.json
sed s/Q1/QN/g -i bbb0.json
sed s/Q2endpoints/$n3\",\"$e3\",\"$s3/g -i bbb0.json
sed s/Q2/QE/g -i bbb0.json

#node 1 with node 0 south and node 2 east neighbors
sed -e s/Q1endpoints/$s0\",\"$e0\",\"$w0/g nodeTemp.json > bbb1.json
sed s/Q1/QS/g -i bbb1.json
sed s/Q2endpoints/$n2\",\"$e2\",\"$s2/g -i bbb1.json
sed s/Q2/QE/g -i bbb1.json

#node 2 with node 3 south and node 1 west neighbors
sed -e s/Q1endpoints/$s3\",\"$e3\",\"$w3/g nodeTemp.json > bbb2.json
sed s/Q1/QS/g -i bbb2.json
sed s/Q2endpoints/$w1\",\"$n1\",\"$s1/g -i bbb2.json
sed s/Q2/QW/g -i bbb2.json

#node 3 with node 2 north and node 0 west neighbors
sed -e s/Q1endpoints/$n2\",\"$e2\",\"$w2/g nodeTemp.json > bbb3.json
sed s/Q1/QN/g -i bbb3.json
sed s/Q2endpoints/$w0\",\"$n0\",\"$s0/g -i bbb3.json
sed s/Q2/QW/g -i bbb3.json


#sed -e s/Q1endpoints/$Nseg/g nodeTemp.json > trial.json
#sed -e s/Q2endpoints/$Eseg/g -i trial.json

#sed s/component0/component0/g -i trial.json
#sed s/n1/"$n1"/g -i trial.json
#sed s/e1/"$e1"/g -i trial.json
#sed s/w1/"$w1"/g -i trial.json

#sed s/bbb3n/"$n3"/g -i trial.json
#sed s/bbb3e/"$e3"/g -i trial.json
#sed s/bbb3s/"$s3"/g -i trial.json
