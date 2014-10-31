#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# exceptions.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-30

import a20micro_gpios as hw
#import a10lime_gpios as hw

# ---------- CREATE BOARD OBJECT

try:
	#board= hw.BOARD()
	#board= hw.BOARD( "/boot/script")
	board= hw.BOARD( "script_test.fex")
	# try to comment out some lines in the gpio_para sections with ';'. 
	# Eg.:	;[gpio_para]
	#		;gpio_num=64
	# or set gpio_used to 0		
	
except GpioUtilsError as err:
	print( "Board creation error. {}".format(err) )	
	exit(1)


try:
	gpio= board.GPIO( "ph00002")	# "ph2"
	gpio= board.GPIO( 644)			# 64
	
except GpioUtilsError as err:	
	print(" Invalid gpio number or name. {}".format(err) )
	exit(2)
	

	
	
