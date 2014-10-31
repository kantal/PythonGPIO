#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# gpioutils.py
# Copyright (C) 2014 Antal Koós
# License: The MIT License (MIT); see the LICENSE.txt file
# Build: 2014-10-23

""" The 'gpioutils' module contains common GPIO related functions, which are not hardware specific.
The functions use the Linux sysfs.

A hardware specific module, e.g.: a10lime_gpios.py, contains hardware specific GPIO data.
Only a hardware specific module must be imported into the user program, and not this 'gpioutils'
module.
You must first instantiate a single BOARD class then one or more GPIO classes.
When you instantiate the BOARD class, you can specify a fex file from which the GPIO data will be read.
If a fex file is not specified, the GPIO data contained by the hardware specific module will be used.

If the instantiation of the BOARD or the GPIO class failed, then a GpioUtilsError exception is thrown.
See the examples, too!

Variables:
	GPIOS: tuples of GPIO number and name;
		 GPIO name can consist of two parts connected by underscore, e.g.: gpio20_ph2 ;
	INTSRC_GNAMES: GPIO names, which can be interrupt sources, the order doesn't matter.
	INTSRC_GNUMS: contains GPIO numbers, which can be interrupt sources, the order doesn't matter.

"""

import errno
import builtins

class GpioUtilsError(Exception):

	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return( repr(self.value) )

builtins.GpioUtilsError= GpioUtilsError		
#------------------------------------------------------------------------------------
	
class GPIO:

	GPIO_UTILS_VERSION="2.0"
	EDGE_TYPES= [ "rising", "falling", "both", "none" ]
	SYSFS_GPIO_DIR= "/sys/class/gpio"	
	
	GPIOS, INTSRC_GNAMES, INTSRC_GNUMS = [], [], []

	def __init__(self, gpiopar):
		""" Create a GPIO object 
		
		Input: a GPIO number or name. A name can consist of two parts connected with '_'.
		It is acceptable if you only specify one of them.
		On error it throws an exception.
		"""
	
		self._num, self._name = self._get_gpio_desc(gpiopar) 
		self._sysfs_name="" 
		self._fd= -1
		if self._num != -1:		
			self._sysfs_name= GPIO.SYSFS_GPIO_DIR+ '/'+ self._name
		else:
			raise GpioUtilsError( "GPIO object can not be created ({})".format(gpiopar) )
		
		
	def name(self):
		""" Returns the GPIO name """
		return( self._name)
		
	def num(self):
		""" Returns the GPIO number """
		return( self._num)
		
	def sysfsname(self):
		""" Returns the GPIO sysfs name """
		return( self._sysfs_name)
		
	def fdsc(self):
		""" Returns the open file descriptor of the sysfs file or -1 """
		return( self._fd)
	
	def export(self):
		""" Export the GPIO
		
		Return a tuple: (True,True) on success else (False, errno) .
		It returns (False,EBUSY) if the GPIO is already exported.
		"""
		return( self._export_gpio( self._num) )
		
		
	def unexport(self):
		""" Unexport the GPIO
		
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._unexport_gpio( self._num) )	
		
		
	def direct_out(self):
		""" Set GPIO direction
		
		It sets the GPIO to output mode.
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._direct_gpio( self._sysfs_name,1) )
		
		
	def direct_in(self):
		""" Set GPIO direction
		
		It sets the GPIO to input mode.
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._direct_gpio( self._sysfs_name,0) )
		
		
	def setv( self, value):
		""" Set the GPIO to 1/0
		
		It sets the GPIO to 1 if the 'value' is True else sets to 0.
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._set_gpio( self._sysfs_name, value) )
		
		
	def setv_1( self):
		""" Set the GPIO to 1
		
		It sets the GPIO to 1.
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._set_gpio( self._sysfs_name,1) )
	
	
	def setv_0( self):
		""" Set the GPIO to 0
		
		It sets the GPIO to 0.
		Return a tuple: (True,True) on success else (False, errno) .
		"""
		return( self._set_gpio( self._sysfs_name,0) )
		
		
	def get(self):
		""" Read the GPIO value
		
		Return a tuple: (True,value) on success else (False, errno) .
		"""
		return( self._get_gpio( self._sysfs_name) )
		
		
	def edge(self, level):
		""" Enble the GPIO as interrupt source
		
		Input: edge - 'rising', 'falling', 'both', 'none'   case insensitive
		Return a tuple: (True,True) on success else (False, errno) .
		It returns (False,EINVAL) if the 'edge' is invalid or the GPIO can't be an interrupt source.
		"""
		return( self._edge_gpio( self._sysfs_name, self._num, level) )	
		
		
	def hold( self):
		""" Open and hold a GPIO on the sysfs
	
		Return a tuple: (True, file object) on success else (False, errno). 
		The file descriptor of the returned file object can be used in the poll() function ( fgpio.fileno() ).
		You must not close the file object directly, use the release() method instead.
		"""
		rslt= self._hold_gpio( self._sysfs_name)
		if rslt[0]:		self._fd= rslt[1]
		return( rslt)
		
		
	def release( self):
		""" Close the open file descriptor """
		if self._fd != -1:	self._fd.close()
		self._fd= -1


	def _get_gpio_desc( self, othergpio):
		""" Get the number and name of 'othergpio' as a tuple

		Input:	a GPIO number or name. A name can consist of two parts connected with '_'.
				One of the parts can be given, too.
		Return: (gpio_num, gpio_name) on success or (-1,None)
		"""
		rslt= (-1, None); 
		if type(othergpio) == str:	
		
			for gnum, gname in  GPIO.GPIOS:
				if gname == othergpio:	rslt=(gnum,gname); break
				p= gname.partition('_')
				if othergpio == p[0]	or	othergpio == p[2]:	rslt=(gnum,gname); break
		else:
			if type(othergpio) == int:
			
				for gnum, gname in  GPIO.GPIOS:
					if gnum == othergpio:		rslt=(gnum,gname); break	
	
		return( rslt)			
		
	
	def _export_gpio( self,gnum):
		
		try:	
			with open( GPIO.SYSFS_GPIO_DIR +'/export','w') as fi:
				fi.write( str(gnum) )
		except IOError as e:
			return( False, e.errno )
					
		return( True, True )
	
	
	def _unexport_gpio( self,gnum):
		
		try:
			with open( GPIO.SYSFS_GPIO_DIR +'/unexport','a') as fi:
				fi.write( str(gnum) )
		except IOError as e:
			return( False,e.errno )	
		
		return( True,True)		
	
	
	def _direct_gpio( self, sysfsgpioname, direction):
		
		try:
			with open( sysfsgpioname+ '/direction', 'w') as fi:
				fi.write( "out" if direction else "in" )
		except IOError as e:	
			return( False, e.errno )	
			
		return( True,True)	
	
	
	def _set_gpio( self, sysfsgpioname, value):
		
		try:
			with open( sysfsgpioname+ '/value', 'a') as fi:
				fi.write( "1" if value else "0" )
		except IOError as e:	
			return( False, e.errno )	
	
		return( True,True)	
	
	
	def _get_gpio(self, sysfsgpioname):
		
		try:
			with open( sysfsgpioname+ '/value', 'r') as fi:
				value= fi.read(1)
		except IOError as e:	
			return( False, e.errno )	
	
		return( True,value)		
		
	
	def _edge_gpio( self, sysfsgpioname, gnum, edge):
		
		edge= edge.lower()
		if edge not in GPIO.EDGE_TYPES: 		return(False,errno.EINVAL)
		if  gnum  not in GPIO.INTSRC_GNUMS:		return(False,errno.EINVAL)
		
		try:
			with open( sysfsgpioname+ '/edge', 'a') as fi:
				fi.write( edge)
		except IOError as e:	
			return( False, e.errno )	
	
		return( True,True)	
		
	
	
	def _hold_gpio( self,sysfsgpioname):
		
		# dont use Python 'with' instruction, the gpio file object must be held open 
		try: 
			fgpio= open( sysfsgpioname+ '/value', 'r')
		except IOError as e:	
			return( False, e.errno )	
				
		return( True,fgpio )
		

# GPIO CLASS END

#------------------------------------------------------------------------------------

def _connect( fex_file, board):

		GPIO.INTSRC_GNAMES=			board._INTSRC_GNAMES
		GPIO.GPIOS= 				board._GPIOS
		GPIO.GPIO_DATA_VERSION=		board._GPIO_DATA_VERSION
		
		if fex_file:		
			rslt= extract_gpios( fex_file)
			if rslt[0]:			
					GPIO.GPIOS= rslt[1]
					GPIO.GPIO_DATA_VERSION= fex_file
			else:
				raise GpioUtilsError( "{} ({})".format( rslt[1],fex_file ) )
		
		GPIO.INTSRC_GNUMS= [ gnum for (gnum,gname) in [ GPIO._get_gpio_desc(0,gn) for gn in GPIO.INTSRC_GNAMES ]  if gname ]
		
		board.INTSRC_GNAMES=		GPIO.INTSRC_GNAMES
		board.GPIOS= 				GPIO.GPIOS
		board.GPIO_DATA_VERSION=	GPIO.GPIO_DATA_VERSION
		board.GPIO_UTILS_VERSION=	GPIO.GPIO_UTILS_VERSION
		board.INTSRC_GNUMS=			GPIO.INTSRC_GNUMS
		
		

	
def extract_gpios( fex_file):
		""" Extract the sysfs gpio name from a fex file
		
		Input: the fex file with full path
		Return a tuple: (True, list_of_gpio_names) on success else (False, description_of_the error)
		The resulting 'list_of_gpio_names' can be put into a hardware specific file.
		"""
		if not fex_file:	return(False,False)
		try:
			fex= open( fex_file,"r")
		except:
			return(False, "Open error: "+fex_file )	
		
		rtcd= (False,"'gpio_para or gpio_num or gpio_used' not found")	
		ngpio, used, count = 0, 0, 0
		rslt= []
		linecount=0
		gpio_para, gpio_used = False, False
		
		for line in fex:
	
			linecount+=1
			line= line.strip()
			if not line or line[0]==';':	continue
			
			if ngpio :
				if line[0] == '[':		break	# another section begins
					
				if not line.startswith("gpio_pin_"):	continue
				
				tmp= line.partition("=")
				gn= tmp[0].partition("pin_")[2]
				tmp= tmp[2].partition(':')[2]
				tmp= tmp.partition('<')[0]
				tmp= tmp.strip().lower()
				# 'pg01' --> 'pg1'
				parts= tmp.partition('0')
				if parts[0].isalpha() and parts[2].isdigit():	tmp= parts[0]+str(int(parts[2]))
				
					
				try:
					gn= int(gn)
				except:
					rtcd= ( False," Error in line "+str(linecount) )
					break
					
				rslt.append( ( gn, "gpio"+str(gn)+"_"+tmp ) )
				
				count+=1		
				if count == ngpio:		
					rtcd= ( True,rslt)
					break
				
				continue
			
			
			if not gpio_para:
				if line.startswith("[gpio_para]"):		gpio_para=True;		
				continue	
			
				
			if not gpio_used:
				
				if line.startswith("gpio_used"):
			
					used= line.partition('=')
					try:
						used= int(used[2])
					except:
						rtcd= (False," Invalid 'gpio_used' in line "+str(linecount) )
						break
						
					if used==0:	
						rtcd= (False, "gpio_used=0")
						break
						
					gpio_used=True	
					
				continue;
				
				
			if line.startswith("gpio_num"):
			
				ngpio= line.partition('=')	
				try:
					ngpio=int(ngpio[2])
				except:
					rtcd= (False,"Invalid 'gpio_num in line "+str(linecount) )	
					break
			
		fex.close()
		if ngpio and ngpio != count:	rtcd= (False, "gpio_num and gpio items not matched")
		return( rtcd)
	
