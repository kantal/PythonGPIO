#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# generic_gpios.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-30

""" Lists of GPIOs 

It must be imported into the user program.
_GPIOS must contain tuples of GPIO number and name;
_INTSRC_GNAMES must contain GPIO names which can be interrupt sources.
"""

import gpioutils

class BOARD:

	#----- DATA BEGIN ---------------------------------------------------
	
	_GPIO_DATA_VERSION= "Generic / 2.0"

	_GPIOS=[ ] # to be filled in or instantiate the BOARD with a fex file
	
	_INTSRC_GNAMES= [ ] # to be filled in

	LED_NAME=""  # onboard LED
	
	#----- DATA END -----------------------------------------------------
	
	def __init__(self, fex_file=None):	# connect the board and the gpioutils
			gpioutils._connect( fex_file, BOARD)
			
	class GPIO( gpioutils.GPIO):
		pass	
	

