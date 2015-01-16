# 2015-01-15 kantal59

CC = arm-linux-gnueabihf-gcc
STRIP = arm-linux-gnueabihf-strip
LIBS= rt

.PHONY: all

all: trigger  a20_c_catch

trigger: trigger.o
	$(CC) -o $@ $@.o $(LIBS:%=-l%)
	$(STRIP) $@

HEADERS = include
vpath %.h $(HEADERS)
a20_c_catch: a20_c_catch.o
	$(CC)  -o $@  $@.o 
	$(STRIP) $@
	
a20_c_catch.o: a20_c_catch.c gpio_a20micro.h gpioutils.h  gpiosysfs.h
	$(CC)  -I$(HEADERS) -c a20_c_catch.c 

.PHONY: clean 
clean:
	rm -f *.o trigger a20_c_catch

