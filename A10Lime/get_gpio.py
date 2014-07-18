#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 2014 by kantal59
# License: GPL

import a10lime_gpios as lime
import sys, errno, os

'''
# in brief:
lime.export_gpio( gnum)
lime.direct_gpio_in( gnum)
rtcd, value = lime.get_gpio( gnum)
print(value)
'''

def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )
	

#-----------  GET THE GPIO NUMBER
if len(sys.argv) !=2:
	print(" Missing command line parameter: gpio_number");   exit(1)
try:
	gnum= int(sys.argv[1])
except:
	print(" Invalid integer string");   exit(2)


#-----------  GET THE GPIO NAME
gname= lime.get_gpio_name( gnum );		
if not gname:	
	print(" Invalid gpio number");   exit(3)

print(" GPIO: {0} [{1}]".format(gnum,gname) )	


#-----------  EXPORT THE GPIO
rtcd, err= lime.export_gpio( gnum)		
if not rtcd:		
	if err == errno.EBUSY:
		perr(" GPIO is already exported", errno.EBUSY)
	else:
		perr( ' Export', err );		exit(4)


#-----------  SET GPIO DIRECTION
rtcd, err= lime.direct_gpio_in( gnum)
if not rtcd:	 
	perr( ' Direction: ', err );		exit(5)

	
#-----------  GET THE VALUE
rtcd, value = lime.get_gpio( gnum)
if not rtcd:
	perr( " Get gpio: ", value);		exit(6)
	
print(" Value: {0}".format( value))
	
	
	
	
