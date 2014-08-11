#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# get_gpio.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

import a10lime_gpios as board
import sys, errno, os

"""
# Example for getting GPIO value
# In brief without error checking and decoration:

board.export_gpio( gnum)
board.direct_gpio_in( gnum)
rtcd, value = board.get_gpio( gnum)
print(value)
"""

#---------- UTILITY TO PRINT ERROR MSG
def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )


#-----------  PRINT VERSION, CHECK THE EXISTENCE OF THE COMMAND LINE PARAMETER
print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

if len(sys.argv) !=2:	
	print(" Missing command line parameter: gpio_number or gpio_name");  exit(1)

#-----------  GET THE GPIO NAME or NUMBER
gnum,gname = None,None

try:	
	gnum= int(sys.argv[1])
except:
	gname= sys.argv[1]
	gnum=  board.get_gpio_num( gname)	
else:	
	gname= board.get_gpio_name( gnum )
	

if not gname or not gnum:	
	print(" Invalid gpio number or name");   exit(2)

print(" GPIO: {0} [{1}]".format(gnum,gname) )	


#-----------  EXPORT THE GPIO
rtcd, err= board.export_gpio( gnum)		
if not rtcd:		
	if err == errno.EBUSY:
		perr(" GPIO is already exported", errno.EBUSY)
	else:
		perr( ' Export', err );		exit(4)


#-----------  SET GPIO DIRECTION
rtcd, err= board.direct_gpio_in( gnum)
if not rtcd:	 
	perr( ' Direction: ', err );		exit(5)

	
#-----------  GET THE VALUE
rtcd, value = board.get_gpio( gnum)
if not rtcd:
	perr( " Get gpio: ", value);		exit(6)
	
print(" Value: {0}".format( value))
	
	
	
	
