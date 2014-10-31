#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# fextract.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-29


import gpioutils 
import sys

fex_file= "script_test.fex"
if len(sys.argv) == 2:
	fex_file= sys.argv[1]
else:
	print("\n Usage: $ ./fextract.py fex_file\n")

rslt= gpioutils.extract_gpios(fex_file) 
print( "\n GPIOs extracted from file '{}':\n rtcd= {}\n {}\n".format( fex_file,rslt[0],rslt[1]) )
