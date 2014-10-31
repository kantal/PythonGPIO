#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# edges.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-29

""" It lists the GPIO numbers which can be interrupt sources, it doesn't handle the hardware, reads only from the GPIO data file. """

import a20micro_gpios as hw
#import a10lime_gpios as hw

#board= hw.BOARD( "script_test.fex")
#board= hw.BOARD( "/boot/script.fex" )
board= hw.BOARD()

print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )
print("\n GPIOS:\n {}\n\n Names of interrupt sources:\n {}".format( board.GPIOS, board.INTSRC_GNAMES ) )
print("\n Ids of available interrupt sources:\n {}".format( board.INTSRC_GNUMS))

print("\n Sorted:\n")
for gnum in sorted(board.INTSRC_GNUMS):
	gn,gname= board.GPIO._get_gpio_desc( 0,gnum)
	print("  {} [{}]".format( gn,gname) )
	



