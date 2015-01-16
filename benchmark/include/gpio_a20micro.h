/* 
 gpio_a20micro.h
 Copyright (C) 2014 Antal Koós
 License: The MIT License (MIT); see the LICENSE.txt file
 Build: 2014-05-01
*/
 
#ifndef _A20MicroGPIO_H
#define _A20MicroGPIO_H

#include <string.h>
#include "gpioutils.h"

const gpiodesc_t  gpiodesc[ ]= /* FEX file:  A20_OLinuxino_Micro_debian_34_90_release_8 */
{ 
		0, "gpio1_pg0","gpio2_pg1","gpio3_pg2","gpio4_pg3","gpio5_pg4","gpio6_pg5","gpio7_pg6","gpio8_pg7","gpio9_pg8",
		"gpio10_pg9","gpio11_pc3","gpio12_pc7","gpio13_pc17","gpio14_pc18","gpio15_pc23","gpio16_pc24","gpio17_ph0",
		"gpio18_ph2","gpio19_ph9","gpio20_ph10","gpio21_ph11","gpio22_ph12","gpio23_ph13","gpio24_ph14","gpio25_ph15",
		"gpio26_ph16","gpio27_ph17","gpio28_ph18","gpio29_ph19","gpio30_ph20","gpio31_ph21","gpio32_ph22","gpio33_ph23",
		"gpio34_ph24","gpio35_ph25","gpio36_ph26","gpio37_ph27","gpio38_pb3","gpio39_pb4","gpio40_pb5","gpio41_pb6",
		"gpio42_pb7","gpio43_pb10","gpio44_pb11","gpio45_pb12","gpio46_pb13","gpio47_pb14","gpio48_pb15","gpio49_pb16",
		"gpio50_pb17","gpio51_pi0","gpio52_pi1","gpio53_pi2","gpio54_pi3","gpio55_pi4","gpio56_pi5","gpio57_pi6","gpio58_pi7",
		"gpio59_pi8","gpio60_pi9","gpio61_pi10","gpio62_pi11","gpio63_pi14","gpio64_pi15"
};

const unsigned int _NGPIO= sizeof( gpiodesc)/sizeof(gpiodesc_t);	// continuous range [0,_NGPIO-1]
const unsigned int _NEDGE= 19;	// non-continuous range!!!
const unsigned int LED_GPIONUM=18;

int get_gpio_num( const char* inpstr)
{
    int i; char* pos, *gstr;
    
    if( *inpstr==0) return(-1); // 'inpstr[0]' must be checked against zero as strncmp( ,,strlen(inpstr)) == 0  if inspstr is empty, see '<*>'
    
    for( i=0;   i<_NGPIO;    i++){
        
       if( (gstr= gpiodesc[i].gpiofname) == 0     ||    (pos= strchr( gstr,'_'))==NULL ) continue;
       if( strncmp( gstr, inpstr, strlen(inpstr) )==0 	// <*> 
       	  ||   strcmp( pos+1, inpstr )==0
          ||   strcmp( gstr, inpstr )==0  )     return(i);
       
    }    
    return(-1);
}


const char* get_gpio_name( int gpionum)
{
    if( gpionum<0 || gpionum>=_NGPIO ) return(NULL);
    
    return( gpiodesc[gpionum].gpiofname );
}



int is_edge_enabled( int gpionum)
{ /* 'ph0', 'ph1', 'ph2', 'ph3', 'ph4', 'ph5', 'ph6', 'ph7', 'ph8', 'ph9', 'ph10', 'ph11', 'ph12', 'ph13', 'ph14',
	 'ph15', 'ph16', 'ph17', 'ph18', 'ph19', 'ph20', 'ph21', 'pi10', 'pi11', 'pi12', 'pi13', 'pi14', 'pi15', 'pi16',
     'pi17', 'pi18', 'pi19'
  */     
    if( (gpionum >= 17 && gpionum <= 31 )	||	 (gpionum >= 61 &&  gpionum <= 64 )  )  return(1);
	return(0);    
}





#endif


