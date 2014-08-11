#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# poll_in_python.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

"""
Example for polling interrupt enabled pin in input mode.
The stdin will be polled, too. Entering 'quit' will stop the program.
 
In brief without error checking and decoration:
 
board.export_gpio( gnum)
board.direct_gpio_in( gnum)
board.edge_gpio( gnum, 'both')
rtcd, fgpio= board.hold_gpio( gnum)
po= select.poll()
po.register( fgpio.fileno(), select.POLLPRI | select.POLLERR)
while True:
	events= po.poll( 5000)
	for fd, ev in events:
		if fd == fgpio.fileno():
			fgpio.seek(0)
			value= fgpio.read()	
			print( value)	

"""

import a10lime_gpios as board
import sys, select, errno, os


def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )
	

#----------- GET THE GPIO NUMBER
print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

if len(sys.argv) !=2:
	print(" Missing command line parameter: gpio_number");    exit(1)

try:
	gnum= int(sys.argv[1])
except:
	print(" Invalid integer string");    exit(2)


#----------- GET THE GPIO NAME
gname= board.get_gpio_name( gnum )	
if not gname:	
	print(" Invalid gpio number");    exit(3)

print(" GPIO: {0} [{1}]".format(gnum,gname) )	


#----------- EXPORT THE GPIO
rtcd, err= board.export_gpio( gnum)		
if not rtcd:		
	if err == errno.EBUSY:
		perr(" GPIO is already exported", errno.EBUSY)
	else:
		perr( ' Export', err );		 exit(4)


#----------- SET GPIO DIRECTION
rtcd, err= board.direct_gpio_in( gnum)
if not rtcd:	 
	perr( ' Direction: ', err );		 exit(5)

	
#----------- SET GPIO EDGE
rtcd, err= board.edge_gpio( gnum, "both") 	
if not rtcd:	 
	perr( ' Edge: ', err );		 exit(6)


#----------- OPEN THE GPIO, GET THE FILE DESCRIPTOR
rtcd, value= board.hold_gpio( gnum)
if not rtcd:	 
	perr( ' Open: ', value ); 	 exit(7)
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
				fgpio.close()
				exit(0)
			continue
			
		if fd == fgpio.fileno():
			fgpio.seek(0)
			v= fgpio.read()	# reading '1\n' or '0\n'
			print( " gpio changed: {0}".format( v ) )	
			continue
	
	
	
