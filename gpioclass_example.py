#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# gpioclass_example.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-29

""" Example for using GPIO class """

import a20micro_gpios as hw
#import a10lime_gpios as hw

def gprint( gpio, msg):
	print( "\t<_{}_>\n\tnum:\t{}\n\tname:\t{}\n\tsysfs name:\t{}\n\tfile descriptor:\t{}\n".format( msg, gpio.num(), gpio.name(), gpio.sysfsname(), gpio.fdsc() ) )


board= hw.BOARD()
#board= hw.BOARD( "script_test.fex")
#board= hw.BOARD( "/boot/script.fex" )

print("\n GPIO data version: {}\n gpioutils version: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )
print("\n GPIOS:\n {}\n\n Names of interrupt sources:\n {}".format( board.GPIOS, board.INTSRC_GNAMES ) )
print("\n Ids of available interrupt sources:\n {}\n".format( board.INTSRC_GNUMS))

if board.LED_NAME:
	led= board.GPIO( board.LED_NAME )
	gprint( led, "LED GPIO")

pg1= board.GPIO( "pg1");		gprint( pg1,"pg1")
gpio2= board.GPIO( "gpio2");	gprint( gpio2,"gpio2")
gpio64= board.GPIO( 64);		gprint( gpio64,"gpio64")

