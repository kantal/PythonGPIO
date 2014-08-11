#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# edges.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

""" It lists the GPIO numbers which can be interrupt sources, it doesn't handle the hardware, reads only from the GPIO the data file. """

import a10lime_gpios as board

print("\n GPIO data version: {},  gpioutils: {}".format( board.GPIO_DATA_VERSION, board.GPIO_UTILS_VERSION) )
print(" Edge enabled GPIOs({0}):".format(len(board.EDGE_ENABLED)) )

for gnum in sorted(board.EDGE_ENABLED):
	print("  {} [{}]".format(gnum, board.get_gpio_name(gnum)))
	

#print( board.EDGE_ENABLED, board.GPIOS)


