#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# blink.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-29

""" Example for LED blinking """

import a20micro_gpios as hw
#import a10lime_gpios as hw
import sys
import time

board= hw.BOARD()
#board= hw.BOARD( "/boot/script.fex" )
#board= hw.BOARD( "script_test.fex")

print("\n GPIO data version: {},  gpioutils: {}\n".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )


if board.LED_NAME:
	led= board.GPIO( board.LED_NAME )
	#led= GPIO( "ph2")
	
	tsleep, period = 0.5, 10
	print(" Blinking the LED[{}/{}] for {} times ...\n".format( led.num(),led.name(),period) )

	led.export()
	led.direct_out()

	for p in range( period):
		led.setv_1()	# turn on the LED
		time.sleep( tsleep)
		led.setv_0()	# turn off
		time.sleep( tsleep)
	
