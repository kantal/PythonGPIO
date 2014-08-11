#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# blink.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

""" Example for LED blinking """

import a10lime_gpios as board
import sys
import time

print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )

#gnum= board.get_gpio_num("gpio20_ph2")
#gnum= board.get_gpio_num("gpio20")
#gnum= board.get_gpio_num("ph2")
#gnum=20
gnum= board.LED_GPIONUM

tsleep, period = 0.5, 10
print("Blinking the LED[{}] for {} times ...".format( gnum,period) )

board.export_gpio( gnum)
board.direct_gpio_out( gnum)

for p in range( period):
	board.set_gpio_1( gnum)	# turn on the LED
	time.sleep( tsleep)
	board.set_gpio_0( gnum)	# turn off
	time.sleep( tsleep)
	
	
	
