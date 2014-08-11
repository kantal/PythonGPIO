#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 2014-07-18 by kantal59
# License: LGPL

import a10lime_gpios as lime
import sys
import time


#gnum= lime.get_gpio_num("gpio20_ph2")
#gnum= lime.get_gpio_num("gpio20")
#gnum= lime.get_gpio_num("ph2")
gnum=20

lime.export_gpio( gnum)
lime.direct_gpio_out( gnum)

for s in range(20):
	lime.set_gpio_1( gnum)	# turn on the LED
	time.sleep(0.5)
	lime.set_gpio_0( gnum)	# turn off
	time.sleep(0.5)
