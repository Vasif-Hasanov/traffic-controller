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
        'sensors':('1443088101SN0','1443088101SN1','1443088101SE0', '1443088101SE1', '1443088101SS0','1443088101SS1', '1443088101SW0',
                   '1443088101SW1', '1443088101SW2'),
        'stateMatrix':('110011000', '010001000', '001100111', '000100001'),
        'minInterval':(200,200,200,200),#1 unit =  0.1 sec
        'maxInterval':(600,600,600,600),
        'threshold1' :(3,3,3,3),
        'threshold2' :(4,4,4,4)
    }
}