# traffic-controller

This project assumes Cities:Skylines is installed with the mod from this repo: https://github.com/visor-vu/Cities-Skylines-Traffic-Manager-President-Edition

  Install python-ZCM (https://github.com/pranav-srinivas-kumar/python-zcm)
------------------------------------------------------------
```sudo pip install virtualenv```

```<project directory> $sudo virtualenv zcmenv```

```<project directory> $source zcm/env/bin/activate```

``` $ pip install zcm ```

browse to zcm install location

```<project directory>/zcmenv/lib/python2.7/site-packages/zcm```

add ```component_instance.name = instance["Name"]``` at line 40 of actor.py

Configure Actors
--------------------
open assignIP.sh and set the IP addresses of the nodes. The following node positions are assumed: 

 ```
 $$$$  1  $$$$$  1  $$$$
 $$$$     $$$$$     $$$$
    2 IC1 3   2 IC2 3
 $$$$     $$$$$     $$$$
 $$$$  0  $$$$$  0  $$$$
 $$$$     $$$$$     $$$$
 $$$$  1  $$$$$  1  $$$$
 $$$$     $$$$$     $$$$
    2 IC0 3   2 IC3 3
 $$$$     $$$$$     $$$$
 $$$$  0  $$$$$  0  $$$$
 ```
 
run assignIP.sh to generate bbb#.json files. Put the json config files on the target machines. 

To start Intersection Controller 0
-------------------------------------

```<project directory>/traffic-controller/cities-skylines2$ zcm --config bbb0.json```

To end the process use

```
$ps -a
$kill -9 <PID of zcm process>
```

