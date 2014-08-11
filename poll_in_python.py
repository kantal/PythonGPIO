#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 2014 by kantal59
# License: GPL

'''
 Example for polling interrupt enabled pin in input mode.
 The stdin will be polled, too. Entering 'quit' will stop the program.
'''

import a10lime_gpios as lime
import sys, select, errno, os


def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )
	

#----------- GET THE GPIO NUMBER
if len(sys.argv) !=2:
	print(" Missing command line parameter: gpio_number");    exit(1)

try:
	gnum= int(sys.argv[1])
except:
	print(" Invalid integer string");    exit(2)


#----------- GET THE GPIO NAME
gname= lime.get_gpio_name( gnum );		
if not gname:	
	print(" Invalid gpio number");    exit(3)

print(" GPIO: {0} [{1}]".format(gnum,gname) )	


#----------- EXPORT THE GPIO
rtcd, err= lime.export_gpio( gnum)		
if not rtcd:		
	if err == errno.EBUSY:
		perr(" GPIO is already exported", errno.EBUSY)
	else:
		perr( ' Export', err );		 exit(4)


#----------- SET GPIO DIRECTION
rtcd, err= lime.direct_gpio_in( gnum);	
if not rtcd:	 
	perr( ' Direction: ', err );		 exit(5)

	
#----------- SET GPIO EDGE
rtcd, err= lime.edge_gpio( gnum, "both"); 	
if not rtcd:	 
	perr( ' Edge: ', err );		 exit(6)


#----------- OPEN THE GPIO, GET THE FILE DESCRIPTOR
rtcd, value= lime.hold_gpio( gnum)
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
	
	
	
