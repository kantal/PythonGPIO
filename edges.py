#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 2014-07-18 by kantal59
# License: LGPL

import a10lime_gpios as lime

print(" Edge enabled GPIOs on A10 Lime:")
for gnum in lime._EDGE_ENABLED:
	print("  {} [{}]".format(gnum, lime.get_gpio_name(gnum)))



