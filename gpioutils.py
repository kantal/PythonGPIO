#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# gpioutils.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

""" This module contains common GPIO related functions, which are not hardware specific.
The functions use the Linux sysfs.
A hardware specific module, e.g.: a10lime_gpios.py, must import this and initialize the 
_GPIOS, _EDGE_ENABLED list variables.
The _GPIOS list must enumerate the GPIO names, the indexes correspond to the GPIO number.
A GPIO name consists of two parts connected by underscore, e.g.: gpio20_ph2 .
The _EDGE_ENABLED list must contain GPIO numbers, which can be interrupt sources, the order doesn't matter.
"""

import errno

GPIO_UTILS_VERSION="1.1"

_EDGE_ENABLED= []
_GPIOS= []

_EDGE_TYPES= [ "rising", "falling", "both", "none" ]
_SYSFS_GPIO_DIR= "/sys/class/gpio"



def get_gpio_num( namestr):
	""" Get the GPIO number
	
	Input: the GPIO name, which can be given by the full name or by one of the partial names.
	Return: the GPIO number on success else 'None'.
	"""
	
	for gnum, gname in enumerate( _GPIOS):
		
			if gname == 0:	continue
			if gname == namestr:	return( gnum)
			p= gname.partition('_')
			if namestr == p[0]	or	namestr == p[2]:	return( gnum)
			
	return( None)



def get_gpio_name( gnum):
	""" Get the GPIO name
	
	Input: the GPIO number.
	Return: the GPIO name if the GPIO number was valid else 'None'.
	"""	
	if gnum < 0  or  gnum >= len( _GPIOS) :		return(None)
	gname= _GPIOS[ gnum]
	if gname == 0:	return(None)
	return( gname)
		
		

def export_gpio( gnum):
	""" Export the GPIO
	
	Input: the GPIO number
	Return a tuple: (True,True) on success else (False, errno) .
	It returns (False,EBUSY) if the GPIO is already exported.
	"""
	try:	
		with open( _SYSFS_GPIO_DIR +'/export','w') as fi:
			fi.write( str(gnum) )
	except IOError as e:
		return( False, e.errno )
				
	return( True, True )



def unexport_gpio( gnum):
	""" Unexport the GPIO
	
	Input: the GPIO number
	Return a tuple: (True,True) on success else (False, errno) .
	"""
	try:
		with open( _SYSFS_GPIO_DIR +'/unexport','a') as fi:
			fi.write( str(gnum) )
	except IOError as e:
		return( False,e.errno )	
	
	return( True,True)		

		

def direct_gpio( gnum, direction):
	""" Set GPIO direction
	
	It sets the GPIO given by the 'gnum' number to output mode if the 'direction' is True else sets to input mode.
	Return a tuple: (True,True) on success else (False, errno) .
	It returns (False,EINVAL) if the given GPIO number was invalid.
	"""
	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL )
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/direction', 'w') as fi:
			fi.write( "out" if direction else "in" )
	except IOError as e:	
		return( False, e.errno )	
		
	return( True,True)	


def direct_gpio_out( gnum):
	""" It sets the GPIO given by the 'gnum' number to output mode. 
	
	It calls direct_gpio( gnum,1).
	Return a tuple: (True,True) on success else (False, errno) .
	"""
	return( direct_gpio( gnum,1))

def direct_gpio_in( gnum):
	""" It sets the GPIO given by the 'gnum' number to input mode. 

	It calls direct_gpio( gnum,0).
	Return a tuple: (True,True) on success else (False, errno) .
	"""
	return( direct_gpio( gnum,0))	



def set_gpio( gnum, value):
	""" Set the GPIO to 1/0
	
	It sets the GPIO given by the 'gnum' number to 1 if the 'value' is True else sets to 0.
	Return a tuple: (True,True) on success else (False, errno) .
	It returns (False,EINVAL) if the given GPIO number was invalid.
	"""
	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL )  
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/value', 'a') as fi:
			fi.write( "1" if value else "0" )
	except IOError as e:	
		return( False, e.errno )	

	return( True,True)	


def set_gpio_1( gnum):
	""" Set the GPIO to 1
	
	It calls set_gpio( gnum,1).
	Return a tuple: (True,True) on success else (False, errno) .
	"""
	return( set_gpio(gnum,1))


def set_gpio_0(gnum):
	""" Set the GPIO to 0
	
	It calls set_gpio( gnum,0).
	Return a tuple: (True,True) on success else (False, errno) .
	"""
	return( set_gpio(gnum,0))		

	
def get_gpio( gnum):
	""" Read the GPIO value
	
	It reads the GPIO given by 'gnum' number.
	Return a tuple: (True,value) on success else (False, errno) .
	It returns (False,EINVAL) if the given GPIO number was invalid.
	"""
	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL)
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/value', 'r') as fi:
			value= fi.read(1)
	except IOError as e:	
		return( False, e.errno )	

	return( True,value)		
	

	
def edge_gpio( gnum, edge):
	""" Enble the GPIO as interrupt source
	
	Input: gnum - the GPIO number;  edge - 'rising', 'falling', 'both', 'none'   case insensitive
	Return a tuple: (True,True) on success else (False, errno) .
	It returns (False,EINVAL) if one of the 'edge' or 'gnum' is invalid or the 'gnum' GPIO can't be an interrupt source.
	"""
	edge= edge.lower()
	if edge not in _EDGE_TYPES: 	return(False,errno.EINVAL)
	gname= get_gpio_name( gnum) 
	if not gname   or  gnum not in _EDGE_ENABLED:		return(False,errno.EINVAL)
	
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/edge', 'a') as fi:
			fi.write( edge)
	except IOError as e:	
		return( False, e.errno )	

	return( True,True)	
	


def hold_gpio( gnum):
	""" Open and hold a GPIO on the sysfs

	Input: the GPIO number
	Return a tuple: (True, file object) on success else (False, errno). 
	The file descriptor of the returned file object can be used in the poll() function ( fgpio.fileno() ).
	You can close the file object as usual: fgpio.close() .
	It returns (False,EINVAL) if the given GPIO number was invalid.
	"""
	# dont use Python 'with' instruction, the gpio file object must be held open 
	gname= get_gpio_name( gnum)
	if not gname: 	return(False,errno.EINVAL)
	try: 
		fgpio= open( _SYSFS_GPIO_DIR+ '/'+ gname+ '/value', 'r')
	except IOError as e:	
		return( False, e.errno )	
			
	return( True,fgpio )
	

		
