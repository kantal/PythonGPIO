
PythonGPIO benchmark 
--------------------
URL: https://github.com/kantal/PythonGPIO


 I wondered how my PythonGPIO module can handle fast interrupts, so I made some kind of test.
It's not an exact quantitative test just a qualitative one.

 An A10Lime board is used to toggle GPIO states, and an A20Micro to detect changes. The pin pairs connected to each other 
on a breadboard using resistors, pull downs, and common ground.
 
 Olimex Linux distributions run on the boards, these are not real time systems and I didn't make any modifications on it:
 file: 		a10_Lime_debian_second_release.7z
 uname -a:	Linux a10Lime 3.4.67+ #4 PREEMPT Sat Dec 14 15:12:10 EET 2013 armv7l GNU/Linux
 
 file:		A20_OLinuxino_Micro_debian_34_90_release_8.7z:
 uname -a:	Linux a20-olimex 3.4.90+ #11 SMP PREEMPT Wed Aug 20 08:20:32 EEST 2014 armv7l GNU/Linux
 
 The test code on the A20 just counts the detected interrupts.
The programs must be run with root privilege, the priority of the Python code can be raised by applying the chrt shell command.
The trigger.c contains GPIO methods based on mmapped(). The catch.py uses the PythonGPIO module which based on the sysfs interface.
There is a sysfs based C-program to catch the interrupts on the A20 side, too, the a20_c.c . 
Which one performs better, the Python code or the C code? 
 

Some results:
 The Python code have good results with GPIO state changes of 2 ms interval, but many changes become unnoticed with 1 ms.
The a20_c.c is more better with 1 ms than the Python code, but does not catch all the interrupts in every test case.
If two instances of the Python code are started for each pin, then the 2 ms interval seems too short.

 The roles of the boards, 'trigger' and 'catcher' can be reversed. For A10 as catcher, 4 ms was a good value.

----------------------------------------------------------------------
--- TEST 1 -----------------------------------------------------------
A10:
----
root@a10Lime:/home/olimex# ./trigger 400000 1000 pi15 pi16

 Number of gpios: 2
 Toggles: 400000
 Interval between toggles: 1000 usecs
 The gpios are: PI15 PI16 
 The estimated test time:  400.000000 seconds ( 6.67 minutes)
 Scheduler:   SCHED_FIFO
 Priority: 99
 
<press Enter to start...>

 working...
 Elapsed time: 409.284957383 seconds

---- 
A20:
---- 
root@a20-olimex:/home/olimex# chrt -f 99 ./catch.py ph0 ph9

 GPIO data version: A20-OLinuXino-MICRO / 2.0,  gpioutils: 2.0

 gpio17_ph0[17]  gpio19_ph9[19] 

 <Press Enter to stop...>

 gpio17_ph0:	388213
 gpio19_ph9:	387910


----------------------------------------------------------------------
--- TEST 2 -----------------------------------------------------------
A10:
----
root@a10Lime:/home/olimex# ./trigger 800000 2000 pi15 pi16

 Number of gpios: 2
 Toggles: 800000
 Interval between toggles: 2000 usecs
 The gpios are: PI15 PI16 
 The estimated test time:  1600.000000 seconds ( 26.67 minutes)
 Scheduler:   SCHED_FIFO
 Priority: 99
 
<press Enter to start...>

 working...
 Elapsed time: 1620.773021033 seconds

---- 
A20:
----
root@a20-olimex:/home/olimex# chrt -f 99 ./catch.py ph0 ph9

 GPIO data version: A20-OLinuXino-MICRO / 2.0,  gpioutils: 2.0

 gpio17_ph0[17]  gpio19_ph9[19] 

 <Press Enter to stop...>

 gpio17_ph0:	800000
 gpio19_ph9:	800000


----------------------------------------------------------------------
--- TEST 3 -----------------------------------------------------------
A10:
----
root@a10Lime:/home/olimex# ./trigger 40000 2000 pi15 pi16

 Number of gpios: 2
 Toggles: 40000
 Interval between toggles: 2000 usecs
 The gpios are: PI15 PI16 
 The estimated test time:  80.000000 seconds ( 1.33 minutes)
 Scheduler:   SCHED_FIFO
 Priority: 99
 
<press Enter to start...>

 working...
 Elapsed time: 81.392177928 seconds

--------------- 
A20 terminal 1:
---------------
root@a20-olimex:/home/olimex# chrt -f 99 ./catch.py ph0 

 GPIO data version: A20-OLinuXino-MICRO / 2.0,  gpioutils: 2.0

 gpio17_ph0[17] 

 <Press Enter to stop...>

 gpio17_ph0:	39996

--------------- 
A20 terminal 2:
---------------
root@a20-olimex:/home/olimex# chrt -f 99 ./catch.py ph9

 GPIO data version: A20-OLinuXino-MICRO / 2.0,  gpioutils: 2.0

 gpio19_ph9[19] 

 <Press Enter to stop...>

 gpio19_ph9:	39126


