/* 
 gpioutils.h
 Copyright (C) 2014 Antal Koós
 License: The MIT License (MIT); see the LICENSE.txt file
 Build: 2014-05-01
 
 GPIO utilities
 
 A) Initialization:
 
 	gpio_struct_setup()
 	export_gpio() / unexport_gpio()
 	direct_gpio()
 	edge_gpio() 
 	
 B1) Synchron mode:
	set_gpio()
	get_gpio()
	
 B2) Asynchron mode:
 
 	fd=hold_gpio()	// open in read only mode
 	
 	select()/pselect()/poll()
 	read( fd,...)
 	
 	release_gpio()
 		
*/
#ifndef _GPIO_UTILS_H
#define _GPIO_UTILS_H

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include "gpiosysfs.h"

#define _BUFFSIZE_      64  

extern const unsigned int _NGPIO;
extern const gpiodesc_t  gpiodesc[ ];


int gpio_struct_setup( unsigned int gnum, const char *gname, gpio_t* gpio)
/*  gnum:   the gpio number or -1;
    gname:  NULL or the name of the gpio as appears in sysfs; 
    gpio:   structure for the gpio data
    Return: 0/-1 on success/error
*/
{
    gpio->gnum= -1;	gpio->gname= NULL;
    if( gnum >= 0 	&& 	 gnum <= _NGPIO){
    
    	if( ( gpio->gname= get_gpio_name( gnum)) == NULL )	return(-1);
    	gpio->gnum= gnum;
    }
    else{
    
    	if( ( gpio->gnum= get_gpio_num( gname)) == -1 )	return(-1);
    	gpio->gname= gpiodesc[ gpio->gnum].gpiofname;
    }
    
    gpio->val=  gpio->dir=  gpio->fd=   -1;   
    return(0);        
}


int export_gpio( gpio_t* gpio)
/*
	Return: 0/errno on success/error	
*/
{
	
    int fd, lth,err;
    char buff[ _BUFFSIZE_ ];
    
    err=0;
    if( (fd=open( SYSFS_GPIO_DIR"/export", O_WRONLY)) == -1 )   return(errno);
    lth= snprintf( buff, sizeof(buff), "%d", gpio->gnum );
    // If the gpio is already exported the write() sets errno to EBUSY.
    if( write( fd, buff, lth) == -1 )	err= errno;
    close(fd);
    return( err);
}


int unexport_gpio( gpio_t* gpio)
/*
	Return: 0/errno on success/error	
*/
{
    int fd, lth, err;
    char buff[ _BUFFSIZE_ ];
    
    err= 0;
    if( (fd=open( SYSFS_GPIO_DIR"/unexport", O_WRONLY)) == -1 )   return(errno);
    lth= snprintf( buff, sizeof(buff), "%d", gpio->gnum );
    // If the gpio is not exported the write() sets errno to EINVAL.
    if( write( fd, buff, lth) == -1 ) 	err= errno;
    close(fd);
    return( err);
}


int direct_gpio( gpio_t* gpio, unsigned int direction)
/*
	Return: 0/errno on success/error	
*/
{
    int fd, err;
    char buff[ _BUFFSIZE_ ];
    
    err= 0;
    snprintf( buff, sizeof(buff), "%s/%s/direction", SYSFS_GPIO_DIR,gpio->gname );
           
    if( (fd=open( buff, O_WRONLY)) == -1 )   return(errno);
    if( direction){   
    
        if( write( fd, "out", 3) == -1 )	err= errno;		else	gpio->dir= 1;
    }
    else{
    
        if( write( fd, "in", 2) == -1 )		err= errno;		else    gpio->dir= 0;
    }    
              
    close(fd);
    return( err);
}


int set_gpio( gpio_t* gpio, unsigned int value)
/*
	Return: 0/errno on success/error	
*/
{
    int fd,err;
    char buff[ _BUFFSIZE_ ];
    char *ostr;
    
    err=0;
    ostr= value > 0 ? "1":"0";
    
   	snprintf( buff, sizeof(buff), "%s/%s/value", SYSFS_GPIO_DIR,gpio->gname );   
   	if( (fd=open( buff, O_WRONLY)) == -1 )   return(errno); 
   	
   	if( write( fd, ostr, 1) == -1 )		err= errno;
   	else
   			gpio->val=  value > 0 ? 1:0 ; 
   		
   	close(fd);
    return( err); 
}


int set_gpio_1( gpio_t* gpio ){		return( set_gpio( gpio,1) );	}
int set_gpio_0( gpio_t* gpio ){		return( set_gpio( gpio,0) );	}


int get_gpio( gpio_t* gpio)
/*
	Return: [0,1]/-1  on success/error
*/
{
    int fd, rtcd;
    char buff[ _BUFFSIZE_ ];
    char val;
    
    snprintf( buff, sizeof(buff), "%s/%s/value", SYSFS_GPIO_DIR,gpio->gname );   
    if( (fd=open( buff, O_RDONLY)) == -1 )   return(-1);    
    rtcd= read( fd, &val, 1);	
    close(fd);    
        
    if( rtcd==-1)	return(-1);
    return( gpio->val =  val=='0' ? 0:1 );
}


int edge_gpio( gpio_t* gpio, int iedge)
/*
	Return: 0/errno on success/error	
*/
{
    int fd,err;
    char buff[ _BUFFSIZE_ ];
    static char *edge[4]={ "none","rising","falling","both" };
    
    err=0;
    snprintf( buff, sizeof(buff), "%s/%s/edge", SYSFS_GPIO_DIR,gpio->gname );   
    
    if( (fd=open( buff, O_WRONLY)) == -1 )   return(errno);
    
    if( iedge<0 || iedge >= sizeof(edge)/sizeof(char*) ) 	return(-1);
    
    if( write( fd, edge[iedge], strlen(edge[iedge]) ) == -1 )	err= errno;
    close(fd);
    return( err);
}


int hold_gpio( gpio_t* gpio)
/*
	Return: 0/ [-1,errno] on success/error	
*/
{
    char buff[ _BUFFSIZE_ ];
    int err;
    
    err= 0;
    if( gpio->fd != -1 )   return(-1);
    snprintf( buff, sizeof(buff), "%s/%s/value", SYSFS_GPIO_DIR,gpio->gname );   
    if( (gpio->fd = open( buff, O_RDONLY) ) == -1 )		err= errno;
    return( err);
}


int release_gpio( gpio_t* gpio)
/*
	Return: 0/ -1 on success/error	
*/
{
    if( gpio->fd <= 0 ) return(-1);
    close( gpio->fd);
    gpio->fd= -1;
    return(0);

}


#endif

