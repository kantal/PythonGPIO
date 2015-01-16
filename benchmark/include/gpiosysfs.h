/*
 gpiosysfs.h
 Copyright (C) 2014 Antal Koós
 License: The MIT License (MIT); see the LICENSE.txt file
 Build: 2014-05-01
*/
#ifndef _GPIOSYSFS_H
#define _GPIOSYSFS_H

#define EDGE_NONE		0
#define EDGE_RISING		1
#define EDGE_FALLING	2
#define EDGE_BOTH		3

#define OUT		1
#define INP		0

#define SYSFS_GPIO_DIR  "/sys/class/gpio"


typedef struct {

                unsigned int gnum;
                const char *gname;   
                int dir;    // direction 0/1    or -1
                int val;    // value    0/1     or -1
                int fd;    // open file descriptor or -1
                
} gpio_t;


typedef struct { 
    char *gpiofname;
} gpiodesc_t;   



int get_gpio_num( const char* );
const char* get_gpio_name( int );
int is_edge_enabled( int );




#endif
