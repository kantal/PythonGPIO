#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 2014-08-03 by kantal59
# a10lime_gpios module
# License: GPL

import errno

_A10LIME_GPIOS= [  
          0, "gpio1_pg0", "gpio2_pg1", "gpio3_pg2", "gpio4_pg3", "gpio5_pg4", "gpio6_pg5", "gpio7_pg6", 
          "gpio8_pg7",  "gpio9_pg8", "gpio10_pg11", "gpio11_pc3", "gpio12_pc18", "gpio13_pc19", "gpio14_pc20",
          "gpio15_pc21", "gpio16_pc22", "gpio17_pc23", "gpio18_pc24", "gpio19_ph0", "gpio20_ph2", "gpio21_ph7",
          "gpio22_ph9", "gpio23_ph10", "gpio24_ph11", "gpio25_ph12", "gpio26_ph13", "gpio27_ph14", "gpio28_ph15",
          "gpio29_ph16", "gpio30_ph17", "gpio31_ph18", "gpio32_ph19", "gpio33_ph20", "gpio34_ph21", "gpio35_ph22",
          "gpio36_ph23", "gpio37_pb3", "gpio38_pb4", "gpio39_pb5", "gpio40_pb6", "gpio41_pb7", "gpio42_pb8", 
          "gpio43_pb10", "gpio44_pb11", "gpio45_pb12", "gpio46_pb13", "gpio47_pb14", "gpio48_pb15", "gpio49_pb16",
          "gpio50_pb17", "gpio51_ph24", "gpio52_ph25", "gpio53_ph26", "gpio54_ph27", "gpio55_pi0", "gpio56_pi1",
          "gpio57_pi2", "gpio58_pi3", "gpio59_pi4", "gpio60_pi5", "gpio61_pi6", "gpio62_pi7", "gpio63_pi8", "gpio64_pi9",
          "gpio65_pi10", "gpio66_pi11", "gpio67_pi12", "gpio68_pi13", "gpio69_pi14", "gpio70_pi15", "gpio71_pi16", 
          "gpio72_pi17", "gpio73_pi18", "gpio74_pi19", "gpio75_pi20", 0, 0, 0, 0, 0 ]

_EDGE_ENABLED= [ g for g in range(19,35) ] + [ g for g in range(65,75) ]
_EDGE_TYPES= [ "rising", "falling", "both", "none", "RISING", "FALLING", "BOTH", "NONE" ]
_SYSFS_GPIO_DIR= "/sys/class/gpio"


def get_gpio_num( namestr):

	for gnum, gname in enumerate( _A10LIME_GPIOS):
		
			if gname == 0:	continue
			if gname == namestr:	return( gnum)
			p= gname.partition('_')
			if namestr == p[0]	or	namestr == p[2]:	return( gnum)
	return( None)



def get_gpio_name( gnum):

		if gnum < 0  or  gnum >= len( _A10LIME_GPIOS) :		return(None)
		gname= _A10LIME_GPIOS[ gnum]
		if gname == 0:	return(None)
		return( gname)
		
		

def export_gpio( gnum):
	try:	
		with open( _SYSFS_GPIO_DIR +'/export','w') as fi:
			fi.write( str(gnum) )
	except IOError as e:
		return( False, e.errno )
				
	return( True, True )



def unexport_gpio( gnum):
	try:
		with open( _SYSFS_GPIO_DIR +'/unexport','a') as fi:
			fi.write( str(gnum) )
	except IOError as e:
		return( False,e.errno )	
	
	return( True,True)		

		

def direct_gpio( gnum, direction):

	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL )
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/direction', 'w') as fi:
			fi.write( "out" if direction else "in" )
	except IOError as e:	
		return( False, e.errno )	
		
	return( True,True)	


def direct_gpio_out( gnum):
	return( direct_gpio( gnum,1))

def direct_gpio_in( gnum):
	return( direct_gpio( gnum,0))	



def set_gpio( gnum, value):

	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL )  
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/value', 'a') as fi:
			fi.write( "1" if value else "0" )
	except IOError as e:	
		return( False, e.errno )	

	return( True,True)	


def set_gpio_1( gnum):
	return( set_gpio(gnum,1))

def set_gpio_0(gnum):
	return( set_gpio(gnum,0))		

	
def get_gpio( gnum):

	gname= get_gpio_name( gnum) 
	if not gname:	return( False,errno.EINVAL)
	try:
		with open( _SYSFS_GPIO_DIR+ '/' +gname+ '/value', 'r') as fi:
			value= fi.read(1)
	except IOError as e:	
		return( False, e.errno )	

	return( True,value)		
	

	
def edge_gpio( gnum, edge):

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
	# dont use Python 'with' instruction, the gpio file object must be held open 
	gname= get_gpio_name( gnum)
	if not gname: 	return(False,errno.EINVAL)
	try: 
		fgpio= open( _SYSFS_GPIO_DIR+ '/'+ gname+ '/value', 'r')
	except IOError as e:	
		return( False, e.errno )	
			
	return( True,fgpio )
	
		
		
