import os

DEVNULL = open(os.devnull, "w")
data = {
    '1443088101':{
        'stateToPhase':{
            '110011000':'GGGggrrrrGGGggrrrr',
            '010001000':'rrrGGrrrrrrrGGrrrr',
            '001100111':'rrrrrGGggrrrrrGGgg',
            '000100001':'rrrrrrrGGrrrrrrrGG'
        },
        'sensors':('1443088101N','1443088101S','1443088101E', '1443088101W'),
        'stateMatrix':('1010', '0101'),
        'minInterval':(200,200),#1 unit =  0.1 sec
        'maxInterval':(600,600),
        'threshold1' :(3,3),
        'threshold2' :(4,4)
    }
}
