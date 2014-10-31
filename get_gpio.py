#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# get_gpio.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-30

import a20micro_gpios as hw
#import a10lime_gpios as hw
import sys, errno, os


"""
# Example for getting GPIO value
# In brief without error checking and decoration:

board= hw.BOARD()
gpio= board.GPIO( gpio_num_or_name )
gpio.export()
gpio.direct_in()
rtcd, value = gpio.get()
print(value)
"""

#---------- UTILITY TO PRINT ERROR MSG

def perr( msg,errn):
	print( msg+ ': '+ os.strerror( errn) )

# ---------- CREATE BOARD OBJECT

board= hw.BOARD()
#board= hw.BOARD( "/boot/script")
#board= hw.BOARD( "script_test.fex")

#-----------  PRINT VERSION, CHECK THE EXISTENCE OF THE COMMAND LINE PARAMETER

print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

if len(sys.argv) !=2:	
	print(" Missing command line parameter: gpio_number or gpio_name");  exit(1)

#-----------  CREATE THE GPIO OBJECT

par=None
try:
	par=int( sys.argv[1])	# gpio number ?
except:
	par= sys.argv[1]		# gpio name

try:
	gpio= board.GPIO( par)
	
except GpioUtilsError as err:	
	print(" Invalid gpio number or name")
	print(err)
	exit(2)
	
	
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
	
#-----------  GET THE VALUE

rtcd, value = gpio.get()
if not rtcd:
	perr( " Get gpio: ", value);		exit(5)
	
print(" Value: {0}".format( value))
	
	
	
	
