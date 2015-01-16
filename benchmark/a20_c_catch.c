/* 
 a20_c_catch.c
 Copyright (C) 2015 Antal Koós
 License: The MIT License (MIT); see the LICENSE.txt file
 Build: 2015-01-13
*/
#include <stdlib.h>
#include <stdio.h>
#include <poll.h>
#include <errno.h>
#include <string.h>		
#include <sched.h>
#include "gpio_a20micro.h"


#define MAXNGPIO	10
#define MAXFD		(MAXNGPIO+1) // +1 for stdin

int main( int argc, char *argv[])
{
    int gnum, rtcd, nfd, timeout, i,index, bytes, ngpio;
    char *endptr;
    char buff[64];
    gpio_t *ptr_gpio;
    
    gpio_t gpios[ MAXNGPIO ];
    unsigned long count[ MAXNGPIO ];
    struct pollfd fdset[ MAXFD ];	


//------------ GET THE PARAMETERS    
    if( argc==1 ){
    
    	printf("Usage: $ ./a20_c_catch	[all|gpio_num_1/gpio_name_1 ... gpio_num_n/gpio_name_n] where n=%d\n", MAXNGPIO);
    	return(1);
    }
    
    // Get the gpio numbers:
    
	for( i=1, index=0;		i< argc  &&	 index< MAXNGPIO ;		i++){
	
			gnum= strtol( argv[i], &endptr, 10);
			if( endptr == argv[i] ){	
				gnum= get_gpio_num( argv[i]);
				if( gnum==-1){ printf(" Invalid number string: %s\n", argv[i] );	continue;	}
			}
			if( !is_edge_enabled( gnum)  ){		printf(" Not edge enabled gpio: %d\n",gnum);	continue; }
			count[ index]= 0;
			gpios[index++].gnum =  gnum;
	}


    if( !index ){	 puts("Nothing to do");		return(2); 	}
    ngpio= index;
    
   // rising the process priority:
 	struct sched_param schedparam;
 	schedparam.sched_priority= sched_get_priority_max(SCHED_FIFO);
 	sched_setscheduler( 0, SCHED_FIFO, &schedparam );
 
 	sched_getparam( 0, &schedparam );
 	printf(" Scheduler: %s SCHED_FIFO\n Priority: %d\n", sched_getscheduler(0)==SCHED_FIFO?" ":"NOT", schedparam.sched_priority);
  
//--------- INITIALISING THE POLL -------------

    memset( (void*)fdset, 0, sizeof(fdset) );
    
    fdset[0].fd = 0;		fdset[0].events = POLLIN;	// stdin
    
    for( i=0, nfd=1;		i< ngpio    && 	 nfd < MAXFD;    	 i++ ){
    
    	ptr_gpio= &gpios[i];
    	if( gpio_struct_setup( ptr_gpio->gnum, NULL, ptr_gpio )!= 0 ){	printf(" Invalid gpio number: %d\n", ptr_gpio->gnum);  return(3); }
    
    	printf(" use gpio %d [ %s ]\n", ptr_gpio->gnum, ptr_gpio->gname );
    
    	if( (rtcd= export_gpio( ptr_gpio)) != 0  &&  rtcd != EBUSY ){	printf(" gpio export error: %s\n", strerror( rtcd) ); return( 4);  	}	
    
	    direct_gpio( ptr_gpio, INP);
    
    	if( (rtcd= edge_gpio( ptr_gpio, EDGE_BOTH )) != 0 ){   	printf(" 'Edge' can't be set: %s\n", strerror( rtcd) );    	return(5); }
    
	    if( (rtcd= hold_gpio( ptr_gpio)) != 0 ){ 	printf( " hold_gpio() error: %s\n", strerror( rtcd) );        return(6);	}
    	fdset[nfd].fd = ptr_gpio->fd;
		fdset[nfd].events = POLLPRI | POLLERR;
		
		bytes=read( fdset[nfd].fd, buff, sizeof(buff)-1);	// reset interrupts
		
    	nfd++;
    
    }

// -------------- PROCESSING -----------
    puts( " <Press Enter to stop...>");
    while(1){

		rtcd = poll(fdset, nfd, -1 );	// timeout=-1 means infinite timeout
	    
    	if (fdset[0].revents & POLLIN) {	// stdin
    		bytes= read( 0, buff, sizeof(buff)-1);
    		break; // stop
    		
    	}
    	
    	for( i=1;	i< nfd;   i++){
    	
    		if ( fdset[i].revents & (POLLPRI | POLLERR) ) {
    	
    			lseek( fdset[i].fd, 0, SEEK_SET);
    			bytes=read( fdset[i].fd, buff, sizeof(buff)-1);
    			count[i-1]++;
    					 
    		}
    	} 
    
    } 
    
    
    for( i=0;	i<ngpio;	i++){
    
       release_gpio( &gpios[i]);
       printf(" %s: \t%lu\n", gpios[i].gname, count[i] );
       
    }   
    
    return(0);
}


