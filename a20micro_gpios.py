#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# a20micro_gpios.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-29

""" Lists of GPIOs for A20-OLinuXino-MICRO

It must be imported into the user program.
_GPIOS must contain tuples of GPIO number and name;
_INTSRC_GNAMES must contain GPIO names which can be interrupt sources.
"""

import gpioutils

class BOARD:

	#----- DATA BEGIN ---------------------------------------------------
	
	_GPIO_DATA_VERSION= "A20-OLinuXino-MICRO / 2.0"

	#_GPIOS=[]	
	_GPIOS=[   #A20_OLinuxino_Micro_debian_34_90_release_8:
			(1, 'gpio1_pg0'), (2, 'gpio2_pg1'), (3, 'gpio3_pg2'), (4, 'gpio4_pg3'), (5, 'gpio5_pg4'), (6, 'gpio6_pg5'), (7, 'gpio7_pg6'),
			(8, 'gpio8_pg7'), (9, 'gpio9_pg8'), (10, 'gpio10_pg9'), (11, 'gpio11_pc3'), (12, 'gpio12_pc7'), (13, 'gpio13_pc17'), 
			(14, 'gpio14_pc18'), (15, 'gpio15_pc23'), (16, 'gpio16_pc24'), (17, 'gpio17_ph0'), (18, 'gpio18_ph2'), (19, 'gpio19_ph9'), 
			(20, 'gpio20_ph10'), (21, 'gpio21_ph11'), (22, 'gpio22_ph12'), (23, 'gpio23_ph13'), (24, 'gpio24_ph14'), (25, 'gpio25_ph15'),
			(26, 'gpio26_ph16'), (27, 'gpio27_ph17'), (28, 'gpio28_ph18'), (29, 'gpio29_ph19'), (30, 'gpio30_ph20'), (31, 'gpio31_ph21'),
			(32, 'gpio32_ph22'), (33, 'gpio33_ph23'), (34, 'gpio34_ph24'), (35, 'gpio35_ph25'), (36, 'gpio36_ph26'), (37, 'gpio37_ph27'),
			(38, 'gpio38_pb3'), (39, 'gpio39_pb4'), (40, 'gpio40_pb5'), (41, 'gpio41_pb6'), (42, 'gpio42_pb7'), (43, 'gpio43_pb10'),
			(44, 'gpio44_pb11'), (45, 'gpio45_pb12'), (46, 'gpio46_pb13'), (47, 'gpio47_pb14'), (48, 'gpio48_pb15'), (49, 'gpio49_pb16'),
			(50, 'gpio50_pb17'), (51, 'gpio51_pi0'), (52, 'gpio52_pi1'), (53, 'gpio53_pi2'), (54, 'gpio54_pi3'), (55, 'gpio55_pi4'),
			(56, 'gpio56_pi5'), (57, 'gpio57_pi6'), (58, 'gpio58_pi7'), (59, 'gpio59_pi8'), (60, 'gpio60_pi9'), (61, 'gpio61_pi10'),
			(62, 'gpio62_pi11'), (63, 'gpio63_pi14'), (64, 'gpio64_pi15')
			]
	
	# According to the A20 User Manual v1.0, interrupt sources can be:
	_INTSRC_GNAMES= [ 'ph0', 'ph1', 'ph2', 'ph3', 'ph4', 'ph5', 'ph6', 'ph7', 'ph8', 'ph9', 'ph10', 'ph11', 'ph12', 'ph13', 'ph14',
					  'ph15', 'ph16', 'ph17', 'ph18', 'ph19', 'ph20', 'ph21', 'pi10', 'pi11', 'pi12', 'pi13', 'pi14', 'pi15', 'pi16',
					  'pi17', 'pi18', 'pi19' ] 

	#LED_NAME=""  # onboard LED
	LED_NAME= 'ph2'	
	
	#----- DATA END -----------------------------------------------------
	
	def __init__(self, fex_file=None):	# connect the board and the gpioutils
			gpioutils._connect( fex_file, BOARD)
			
	class GPIO( gpioutils.GPIO):
		pass	
	
	
