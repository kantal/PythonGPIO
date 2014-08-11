#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# a10lime_gpios.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-08-11

""" Lists of GPIOs for A10-OLinuXino-LIME

It must be imported into the user program and this will import the 'gpioutils' modul.
"""

from gpioutils import *
import gpioutils

GPIO_DATA_VERSION= "A10-OLinuXino-LIME / 1.1"

# (A)(A10Lime specific) Available GPIOs according to "GPIO under Linux" on https://www.olimex.com/wiki/A10-OLinuXino-LIME  :
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
          "gpio72_pi17", "gpio73_pi18", "gpio74_pi19", "gpio75_pi20" ]

# (B)(A10 CPU specific) According to the A10 User Manual v1.20,  interrupt sources can be:
_girqs=[ "ph7","ph6","ph5","ph4","ph3","ph2","ph1","ph0","ph15","ph14","ph13","ph12","ph11","ph10","ph9","ph8",
	   	  "ph21","ph20","ph19","ph18","ph17","ph16","pi15","pi14","pi13","pi12","pi11","pi10","pi19","pi18","pi17","pi16"]
	

GPIOS= _A10LIME_GPIOS
gpioutils._GPIOS = GPIOS
# According to the intersection of (A) and (B), interrupt sources on A10Lime can be:
EDGE_ENABLED= [ _gnum for _gnum in [ gpioutils.get_gpio_num( _gname ) for _gname in _girqs ] 	if _gnum  ] # it uses gpioutils._GPIOS !

gpioutils._EDGE_ENABLED = EDGE_ENABLED

LED_GPIONUM= 20 # onboard LED


