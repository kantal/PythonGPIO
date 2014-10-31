#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# poll_in_python.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-30

"""
Example for polling interrupt enabled pin in input mode.
The stdin will be polled, too. Entering 'quit' will stop the program.
 
In brief without error checking and decoration:

gpio= board.GPIO( gpio_num_or_name) 
gpio.export()
gpio.direct_in()
gpio.edge("both")
rtcd, value= gpio.hold()
fgpio= value
po= select.poll()
po.register( fgpio.fileno(), select.POLLPRI | select.POLLERR)
while True:
	events= po.poll( 5000)
	for fd, ev in events:
		if fd == fgpio.fileno():
			fgpio.seek(0)
			val= fgpio.read()	
			print( val)	

"""

import a20micro_gpios as hw
#import a10lime_gpios as hw
import sys, select, errno, os

#---------- UTILITY TO PRINT ERROR MSG
def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )
	

# ---------- CREATE BOARD OBJECT
board= hw.BOARD()

#-----------  PRINT VERSION, CHECK THE EXISTENCE OF THE COMMAND LINE PARAMETER

print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

if len(sys.argv) !=2:
	print(" Missing command line parameter: gpio_number or gpio_name");    exit(1)

#-----------  CREATE THE GPIO OBJECT

par=None
try:
	par=int( sys.argv[1])	# gpio number ?
except:
	par= sys.argv[1]		# gpio name

try:
	gpio= board.GPIO( par)
except:	
	print(" Invalid gpio number or name");   exit(2)
	
	
print(" GPIO: {0} [{1}]".format( gpio.name(),gpio.num() ) )	

#-----------  EXPORT THE GPIO

rtcd, err= gpio.export()		
if not rtcd:		
	if err == errno.EBUSY:
		perr(" GPIO is already exported", errno.EBUSY)
	else:
		perr( ' Export', err );		exit(3)


#-----------  SET GPIO DIRECTION

rtcd, err= gpio.direct_in()
if not rtcd:	 
	perr( ' Direction: ', err );		exit(4)
	
	
#----------- SET GPIO EDGE

rtcd, err= gpio.edge("both") 	
if not rtcd:	 
	perr( ' Edge: ', err );		 exit(5)


#----------- OPEN THE GPIO, GET THE FILE DESCRIPTOR

rtcd, value= gpio.hold()
if not rtcd:	 
	perr( ' Open: ', value ); 	 exit(6)

fgpio= value

#----------- SET POLL

po= select.poll()
po.register( fgpio.fileno(), select.POLLPRI | select.POLLERR)
po.register( 0, select.POLLIN)	# stdin

	
#----------- POLLING

while True:
	events= po.poll( 5000)	# msecs
	
	print(" events: {0}".format( events) )
	if not events:
		print(" timeout")
		continue
			
	for fd, ev in events:
	
		if fd == 0:
			s= input()
			print( " input from stdin: {0}".format( s) )
			if s == 'quit':	
				gpio.release()
				exit(0)
			continue
			
		if fd == fgpio.fileno():
			fgpio.seek(0)
			val= fgpio.read()	# reading '1\n' or '0\n'
			print( " gpio changed: {0}".format( val ) )	
			continue
	
	
	
