#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# a10lime_gpios.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-30

""" Lists of GPIOs for A10-OLinuXino-LIME

It must be imported into the user program. 
_GPIOS must contain tuples of GPIO number and name;
_INTSRC_GNAMES must contain GPIO names which can be interrupt sources.
"""

import gpioutils

class BOARD:

	#----- DATA BEGIN ---------------------------------------------------
	
	_GPIO_DATA_VERSION= "A10-OLinuXino-LIME / 2.0"

	#_GPIOS=[]	
	_GPIOS=[ # a10Lime_debian_second_release:
			 (1, 'gpio1_pg0'), (2, 'gpio2_pg1'), (3, 'gpio3_pg2'), (4, 'gpio4_pg3'), (5, 'gpio5_pg4'), (6, 'gpio6_pg5'), (7, 'gpio7_pg6'),
			 (8, 'gpio8_pg7'), (9, 'gpio9_pg8'), (10, 'gpio10_pg11'), (11, 'gpio11_pc3'), (12, 'gpio12_pc18'), (13, 'gpio13_pc19'), 
			 (14, 'gpio14_pc20'), (15, 'gpio15_pc21'), (16, 'gpio16_pc22'), (17, 'gpio17_pc23'), (18, 'gpio18_pc24'), (19, 'gpio19_ph0'),
			 (20, 'gpio20_ph2'), (21, 'gpio21_ph7'), (22, 'gpio22_ph9'), (23, 'gpio23_ph10'), (24, 'gpio24_ph11'), (25, 'gpio25_ph12'),
			 (26, 'gpio26_ph13'), (27, 'gpio27_ph14'), (28, 'gpio28_ph15'), (29, 'gpio29_ph16'), (30, 'gpio30_ph17'), (31, 'gpio31_ph18'),
			 (32, 'gpio32_ph19'), (33, 'gpio33_ph20'), (34, 'gpio34_ph21'), (35, 'gpio35_ph22'), (36, 'gpio36_ph23'), (37, 'gpio37_pb3'),
			 (38, 'gpio38_pb4'), (39, 'gpio39_pb5'), (40, 'gpio40_pb6'), (41, 'gpio41_pb7'), (42, 'gpio42_pb8'), (43, 'gpio43_pb10'),
			 (44, 'gpio44_pb11'), (45, 'gpio45_pb12'), (46, 'gpio46_pb13'), (47, 'gpio47_pb14'), (48, 'gpio48_pb15'), (49, 'gpio49_pb16'),
			 (50, 'gpio50_pb17'), (51, 'gpio51_ph24'), (52, 'gpio52_ph25'), (53, 'gpio53_ph26'), (54, 'gpio54_ph27'), (55, 'gpio55_pi0'),
			 (56, 'gpio56_pi1'), (57, 'gpio57_pi2'), (58, 'gpio58_pi3'), (59, 'gpio59_pi4'), (60, 'gpio60_pi5'), (61, 'gpio61_pi6'),
			 (62, 'gpio62_pi7'), (63, 'gpio63_pi8'), (64, 'gpio64_pi9'), (65, 'gpio65_pi10'), (66, 'gpio66_pi11'), (67, 'gpio67_pi12'),
			 (68, 'gpio68_pi13'), (69, 'gpio69_pi14'), (70, 'gpio70_pi15'), (71, 'gpio71_pi16'), (72, 'gpio72_pi17'), (73, 'gpio73_pi18'),
			 (74, 'gpio74_pi19'), (75, 'gpio75_pi20')   
			]
			
	# According to the A10 User Manual v1.20,  interrupt sources can be:
	_INTSRC_GNAMES= [ 'ph0', 'ph1','ph2','ph3', 'ph4','ph5', 'ph6', 'ph7', 'ph8', 'ph9','ph10', 'ph11', 'ph12', 'ph13', 'ph14', 
					  'ph15', 'ph16', 'ph17', 'ph18', 'ph19', 'ph20', 'ph21','pi10', 'pi11', 'pi12', 'pi13', 'pi14', 'pi15', 'pi16',
					  'pi17', 'pi18', 'pi19' ] 

	#LED_NAME=""  # onboard LED
	LED_NAME= 'ph2'	
	
	#----- DATA END -----------------------------------------------------
	
	def __init__(self, fex_file=None):	# connect the board and the gpioutils
			gpioutils._connect( fex_file, BOARD)
			
	class GPIO( gpioutils.GPIO):
		pass	
	

