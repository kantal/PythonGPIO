##PythonGPIO
###Python GPIO modules for OLIMEX boards

It uses the Linux sysfs, so it may be slower than other implementations with direct register access. It is tested on Python 3.x.
There is no install script; the modules must be copied into the directory of your program or a directory listed in sys.path.

Program files:
- hardware specific:
	* a10lime_gpios.py
- common:
	* gpioutils.py
- examples:
	* blink.py
	* get_gpio.py
	* poll_in_python.py
	* edges.py	

You must import one of the hardware specific files only. For help run e.g:	
- pydoc a10lime_gpios	
- pydoc gpioutils

License: The MIT License (MIT); see the LICENSE.txt file
