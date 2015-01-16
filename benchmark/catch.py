#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# catch.py
# Copyright (C) 2015 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2015-01-15

# chrt -f 99 ./catch.py gpio1 gpio2 ...


import sys, select, errno, os
from subprocess import *

pip = Popen(["uname",'-a'], stdout=PIPE, universal_newlines=True)
output, errs = pip.communicate()
if 'a10' in output.lower():
	import a10lime_gpios as hw
else:	
	import a20micro_gpios as hw
	


#---------- UTILITY TO PRINT ERROR MSG
def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )

# ---------- CREATE BOARD OBJECT
board= hw.BOARD()

#-----------  PRINT VERSION, CHECK THE EXISTENCE OF THE COMMAND LINE PARAMETER
print("\n GPIO data version: {},  gpioutils: {}\n".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

if len(sys.argv) < 2:
	print(" Missing command line parameter: gpio_1 ... gpio_n\t where 'gpio_x' can be a gpio number or name")    
	exit(1)

#-----------  CREATE THE GPIO OBJECTS

lgpio= []   # gpio objects
lcnt= []    # interrupt counters

for i in range( 1,len(sys.argv)):
	par= None
	try:
		par= int( sys.argv[i])	# gpio number ?
	except:
		par= sys.argv[i]		# gpio name

	try:
		gpio= board.GPIO( par)
	except:	
		print("\n Invalid gpio number or name: {}".format( sys.argv[i]) )   
		exit(2)
	
	lgpio.append( gpio)
	print(" {}[{}]".format( gpio.name(),gpio.num() ), end=' ' )

print("\n")

#-----------  SETUP THE GPIOS

for gpio in lgpio:
	
	rtcd, err= gpio.export()
	if not rtcd  and   err != errno.EBUSY:
		perr( ' Export error', err )
		exit(3)

	rtcd, err= gpio.direct_in()
	if not rtcd:
		perr( ' Direction error: ', err )
		exit(4)

	rtcd, err= gpio.edge("both")
	if not rtcd:
		perr( ' Edge error: ', err )
		exit(5)


	rtcd, value= gpio.hold()
	if not rtcd:
		perr( ' Open: ', value )
		exit(6)
	
	lcnt.append(0)

#----------- SET POLL

po= select.poll()
po.register( 0, select.POLLIN)	# stdin
for gpio in lgpio:
	po.register( gpio.fdsc().fileno(), select.POLLPRI | select.POLLERR)
	# reset interrupts:
	gpio.fdsc().read()	
	
#----------- POLLING
print( " <Press Enter to stop...>")
end=False
while True:
	events= po.poll()
	
	for fno, ev in events:
	
		if fno == 0:     # 'Enter' is pressed
			end= True
			break
			
		for i,gpio in enumerate(lgpio):
			if gpio.fdsc().fileno() == fno:
				gpio.fdsc().seek(0)
				gpio.fdsc().read()	
				lcnt[i] += 1
				
	if end:	break
	

for i,gpio in enumerate(lgpio):
	gpio.release()
	print(" {}:\t{}".format( gpio.name(),lcnt[i] ) )
print("")

