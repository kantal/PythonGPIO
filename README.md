##PythonGPIO
###Python GPIO modules for OLIMEX boards

WARNING: This 2.0 version and the previous 1.1 version are COMPLETELY INCOMPATIBLE !

It uses the Linux sysfs, so it may be slower than other implementations with direct register access. It is tested on Python 3.x.
There is no install script; the modules must be copied into the directory of your program or a directory listed in sys.path.
You must import one of the hardware specific files.
Please, look over the examples,too.
NOTE for the examples: you must change the import statement corresponding to your hardware!

FILES:
- hardware specific:
	* a10lime_gpios.py
	* a20micro_gpios.py
	* generic_gpios.py
- common:
	* gpioutils.py
- examples:
	* gpioclass_example.py
	* exceptions.py
	* blink.py
	* get_gpio.py
	* poll_in_python.py
	* edges.py	
- documentation:
	* README.md
	* ReleaseNotes.txt	
	* Guide.txt
- others:
	* script_test.fex	


License: The MIT License (MIT); see the LICENSE.txt file

