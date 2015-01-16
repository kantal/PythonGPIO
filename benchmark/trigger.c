/* 
 trigger.c
 Copyright (C) 2015 Antal Koós
 License: The MIT License (MIT); see the LICENSE.txt file
 Build: 2015-01-15

  Compile with -lrt
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <inttypes.h>
#include <string.h>
#include <time.h>
#include <sched.h>

#define PIO_BASE		0x01C20800 
#define PIO_SIZE		1024			// bytes

#define INPUT			0b000
#define OUTPUT			0b001

void *pmap;
uint8_t *ptr_piobase;

typedef struct{

	uint32_t cfg[4];
	uint32_t data;
	uint32_t drive[2];
	uint32_t pull[2];

} pioctrl_t;

typedef struct {

	pioctrl_t *ppio;
	int bank;
	int num;
	int cfgidx; // config register index
	int shift;  // bit shift in config register

} gpio_t;


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        uint32_t get_cfg( gpio_t *gpio)
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
{
	return( (gpio->ppio->cfg)[ gpio->cfgidx ] >> gpio->shift );
}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	void set_cfg( gpio_t *gpio, uint8_t newcfg)
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
{
	newcfg&= 0b111;
	uint32_t tmp= (gpio->ppio->cfg)[ gpio->cfgidx ]  &  ~(0b111 << gpio->shift);
	
	(gpio->ppio->cfg)[ gpio->cfgidx ] =	 tmp  |  (newcfg << gpio->shift) ;
}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	unsigned int get_value( gpio_t *gpio)
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
{
	return( (gpio->ppio->data >> gpio->num) & 1 );
}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	void set_value(  gpio_t *gpio, int value )
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
{
	if( value) gpio->ppio->data |= (1 << gpio->num);
	else
		gpio->ppio->data &= ~ (1 << gpio->num);
}

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    gpio_t* create_gpio( char *str, gpio_t *gpio)   
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// E.g.: in *str="PH2", the gpionum is 2 corresponding to cfg[0] in bank 7. The bank is specified by 'PH'.
{
    char *ptr;
    if( toupper(*(ptr=str) ) != 'P' 	||	 strlen(ptr) < 3 )		return(NULL);
    char bank= toupper(ptr[1]);
    if( bank < 'A'	||	bank > 'I' )	return(NULL);
    int num= strtoul( ptr+2,NULL,10);
    if( num > 31	) return(NULL);

    bank -= 'A';
    gpio->ppio= ( pioctrl_t*) ( ptr_piobase + bank * sizeof(pioctrl_t) );
    gpio->num= num;
    gpio->bank= bank;
    gpio->cfgidx= num/8;
    gpio->shift= 4*(num%8);
    return( gpio);
}

// %%%%%%%%%%%%%%%% 	
    int init()
// %%%%%%%%%%%%%%%%
{
 int fd;
 
 if( (fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1 ){		perror("/dev/mem open error");		return(-1);	}
 
 off_t offset= PIO_BASE;
 off_t newoffset= PIO_BASE & ~(sysconf( _SC_PAGE_SIZE)-1);
 size_t shift= offset-newoffset;
 
 pmap = mmap( NULL, PIO_SIZE + shift, PROT_READ | PROT_WRITE, MAP_SHARED, fd, newoffset );  
 if( pmap == MAP_FAILED ){	perror("mmap error");	close(fd);	return(-2);	}	
 ptr_piobase= pmap + shift;
 
 return(0);
}
 	
 		
// %%%%%%%%%%%%%%%%%%%%%%%%

#define MAXGPIO		16

// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		int main( int argc, char *argv[])
// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
{

 int i,ngpio;
 char *ptr;
 gpio_t *pend, *pgpio;
 
 gpio_t GPIO[ MAXGPIO];
 
//-------------------------
 if( argc<4 ){	
 	printf(" Usage: $ ./trigger    count  useconds  gpio_name1 gpio_name2 ... gpio_name%d\n"
		"\tcount= number of toggles\n"
		"\tuseconds= micro seconds between toggles\n"
		"\tgpio_name can be Pxn where x=A,B,C,D,E,F,G,H,I and n= 0-31 \n",MAXGPIO); 
 	exit(1);	
 }
//-------------------------
 
 if( init() != 0 ) exit(1);

//--------------------------

 unsigned long count= strtoul( argv[1],NULL,10);
 if( count<= 1){		puts(" count must be >= 2");	 exit(1);	}
 unsigned long usec= strtoul( argv[2],NULL,10);

 ngpio=0;
 for( i=3;		i<argc  &&   ngpio<MAXGPIO;		 i++){
 
 		if( create_gpio( argv[i], &GPIO[ ngpio] ) ==  NULL )  continue;
 		set_cfg( &GPIO[ ngpio], OUTPUT);
 		ngpio++;
 }

 if( ngpio==0){ puts(" number of gpios is 0");	exit(4);	}

//------------------------

 printf( "\n Number of gpios: %d\n Toggles: %lu\n Interval between toggles: %lu usecs\n", ngpio,count,usec);
 printf( " The gpios are: ");
 for( i=0;	i< ngpio;	i++)	printf( "P%c%d ", GPIO[i].bank+'A', GPIO[i].num);
 float etime= (float)count*usec/1000000;
 float mins= etime/60;
 printf("\n The estimated test time:  %.6f seconds ( %.2f minutes)\n", etime,mins );
 
 // rising the process priority:
 struct sched_param schedparam;
 schedparam.sched_priority= sched_get_priority_max(SCHED_FIFO);
 sched_setscheduler( 0, SCHED_FIFO, &schedparam );
 
 sched_getparam( 0, &schedparam );
 printf(" Scheduler: %s SCHED_FIFO\n Priority: %d\n", sched_getscheduler(0)==SCHED_FIFO?" ":"NOT", schedparam.sched_priority);
 
//------------------------

 struct timespec tim,tstart,tstop;
 
 tim.tv_sec= usec/1000000;
 tim.tv_nsec=  (usec - tim.tv_sec*1000000)*1000;       
 puts(" \n<press Enter to start...>");
 getchar();
 puts(" working...");
 
//--- START -------------
 clock_gettime( CLOCK_MONOTONIC, &tstart);  
 for( i= 0;		i< count/2;		i++){
 
	pgpio= GPIO;	pend= GPIO + ngpio; 
	while( pgpio < pend){  		set_value( pgpio, 1); 	pgpio++; 	}
	
	clock_nanosleep( CLOCK_MONOTONIC,0,&tim,NULL);
	
	pgpio= GPIO;	pend= GPIO + ngpio; 
	while( pgpio < pend){  		set_value( pgpio, 0);  	pgpio++;	}
	
	clock_nanosleep( CLOCK_MONOTONIC,0,&tim,NULL);
 }
 
 clock_gettime( CLOCK_MONOTONIC, &tstop);  
//--- STOP --------------
 
 tstop.tv_sec-= tstart.tv_sec;
 if( tstop.tv_nsec >= tstart.tv_nsec){
 
 	tstop.tv_nsec-= tstart.tv_nsec;
 }	
 else{
	tstop.tv_sec--;		tstop.tv_nsec= 1000000000 - (tstart.tv_nsec-tstop.tv_nsec) ;
 }	

 printf(" Elapsed time: %1$lu.%2$09lu seconds\n\n", tstop.tv_sec, tstop.tv_nsec);
 
 return(0);
 
}

