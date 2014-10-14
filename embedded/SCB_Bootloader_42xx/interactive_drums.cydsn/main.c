/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include <project.h>
#include <stdint.h>
#include <stdio.h>
#include "drums.h"

#define NUM_DRUMS_ENABLED 1
//#define CALLIBRATE_FLAG
//#define DEBUG_ON

void pullPacketInterrupt(void);

ringBuf_t ringBuf;

/* Starting State */
volatile state_t state = SHOW_MODE_S;

uint16_t hit_mask = 0;
uint16_t drum_thresholds[NUM_DRUMS_ENABLED];

char string_buffer[50];

uint16_t timer_period = 3200;
extern const uint16_t pwm_array[16];


/* Interrupt used to process a packet */ 
CY_ISR_PROTO(beat_interrupt);
CY_ISR(beat_interrupt){
    uint8_t i;
    packet_t temp_packet;
    
    switch(state){
        case BUF_LOAD_S:
            /* Wait for packets to fill up the buffer */
        break;
        
        case LEAD_MODE_S:
            /* Process a packet, send back the restults from ADC thresholds */
            temp_packet = ringBuf_get(&ringBuf);
            if(temp_packet.packet.control != EMPTY_ERR){
                temp_packet.packet.drums = hit_mask;
                for(i = 0; i < 4; i++) 
                    UART_UartPutChar(temp_packet.byte[i]);
            }
        break;
        
        case WAIT_MODE_S:
            /* if you detected a hit send back a packet */
            temp_packet = ringBuf_peek(&ringBuf);
            if( (!temp_packet.packet.drums) || (hit_mask && temp_packet.packet.drums)){
                temp_packet = ringBuf_get(&ringBuf);
                if(temp_packet.packet.control != EMPTY_ERR){
                    temp_packet.packet.drums = hit_mask;
                    for(i = 0; i < 4; i++) 
                        UART_UartPutChar(temp_packet.byte[i]);
                }
            }
        break;
            
        default:
            /* SHOW_MODE_S */
            break;
                
    } /* Switch (state) END */
    
    hit_mask = 0;
    timer_Start();
} 

void pullPacketInterrupt(void){
    uint8_t i;
    packet_t temp_packet;
    
    if(0u != (UART_GetRxInterruptSourceMasked() & UART_INTR_RX_TRIGGER)){
        /*
         *  Pull Packet from the Buffer
        */
        if(UART_SpiUartGetRxBufferSize() > 3){
            for(i = 0; i < 4; i++){   
                temp_packet.byte[i] = (uint8_t) (UART_UartGetByte() & 0xFF);
            }
        }
            
        /*
         * When the buffer is full enough, start the song
        */ 
        if(state == BUF_LOAD_S){
            if(ringBuf.count >= MIN_BUF)
                state = WAIT_MODE_S;
        }
        
        /*
         *  Switch Statement for changing state
        */
        switch(temp_packet.packet.control){
            case EMPTY:
                ringBuf_put(&ringBuf, temp_packet);
                break;
                
            case RESET:
                ringBuf_flush(&ringBuf);
                state = BUF_LOAD_S;
                break;
                
            case PAUSE:
                state = PAUSE_S;
                break;
                
            case WAIT_MODE:
                state = WAIT_MODE_S;
                break;
                
            case LEAD_MODE:
                state = LEAD_MODE_S;
                break;
             
            default:
                if(!ringBuf_full(&ringBuf))
                    ringBuf_put(&ringBuf, temp_packet);
                break;
        }
        
        UART_ClearRxInterruptSource(UART_INTR_RX_ALL);
    }
}

int main(){
    /*
     *  Variable Decleration
    */
    int16_t i;
    uint16_t drums;
    
    uint8_t freePwm;
    uint8_t time_in_packet, last_time_in_packet;
    
    /*
     * Setup Code
    */
    UART_SetCustomInterruptHandler(&pullPacketInterrupt);
    ringBuf_init(&ringBuf);
    UART_Start();
    
    
    /* Start the 3 PWM Channels */
    RED_A_Start();
    RED_B_Start();
    RED_C_Start();
    
    /* Start timer running for 3200 Ticks */
    /* 150 BPM, 600 PPM, 10PPS, 3200 Ticks Per Packet */
    timer_WritePeriod(3200);
    timer_Start();
    
    tick_StartEx(beat_interrupt);
    
    /* Start the ADC */
    ADC_Start();
    ADC_StartConvert();
    
    /* Callibrate the ADC */
#ifdef CALLIBRATE_FLAG
    uint16_t low_limit = 0;
    for(i = 0; i < NUM_DRUMS_ENABLED; i ++){
        drum_thresholds[i] = 0x07FF;
        timer_WriteCounter(0xFFFE);
        GREEN_Write( 1 << i );
        /* 0x03FF - to give the timer enough time if a Conversion takes a long time */
        while(timer_ReadCounter() > 1){ 
            if(ADC_IsEndConversion(ADC_RETURN_STATUS)){
                drum_thresholds[i] = (ADC_GetResult16(i) < drum_thresholds[i]) ? ADC_GetResult16(i) : drum_thresholds[i];
            }
        }
        drum_thresholds[i] += (0x0710 - drum_thresholds[i] ) / 2;
    }
    
    /* Loop and find the highest threshold */
    for(i = 0; i < NUM_DRUMS_ENABLED; i++){
        low_limit = (drum_thresholds[i] > low_limit) ? drum_thresholds[i] : low_limit;
    }
    
    low_limit += 0x01A;
    ADC_SetLowLimit(low_limit);
#else
    ADC_SetLowLimit(0x6E0);
#endif

#ifdef DEBUG_ON
    char buff[30];
    sprintf(buff, "%x %x %x %x %x\n", 
        drum_thresholds[0], 
        drum_thresholds[1], 
        drum_thresholds[2], 
        drum_thresholds[3], 
        low_limit); 
    UART_UartPutString(buff);
#endif
    
    timer_WritePeriod(3200);
    CyGlobalIntEnable; 
    
    for(;;)
    {
        
        /* Some Hit Detection Magic */        
        if(ADC_IsEndConversion(ADC_RETURN_STATUS)){
            for(i = 0; i < NUM_DRUMS_ENABLED; i++ ){
                hit_mask |= (ADC_GetResult16(i) < drum_thresholds[i]) << i;
            }
#ifdef DEBUG_ON
            if(hit_mask){
                sprintf(buff, "%x %x %x %x\n", 
                    ADC_GetResult16(0), 
                    ADC_GetResult16(1), 
                    ADC_GetResult16(2), 
                    ADC_GetResult16(3)); 
                UART_UartPutString(buff);
            }
    
#endif
        }
        
        /* Start by looking through future packets to set the leds */
       if((state == LEAD_MODE_S) || (state == WAIT_MODE_S)){
            time_in_packet = timer_ReadCounter() / (timer_period / 4);
            if(time_in_packet != last_time_in_packet){
                freePwm = 0x07;

                for(i = MAX_PACKET_PARSE ; i > 0; i--){
                    drums = ringBuf.buf[WRAP(ringBuf.tail + i)].packet.drums;
                    freePwm &= ~set_red_pwm(freePwm, (uint8_t) drums, i, time_in_packet);
                } 
                
                last_time_in_packet = time_in_packet;
                GREEN_Write(ringBuf.buf[ringBuf.tail].packet.drums);

            }    
        }
        
        if( state == SHOW_MODE_S ){
            GREEN_Write(hit_mask);
        }
            
        /* If you aren't running make sure to turn off the leds */
        else {
            REG_A_Write(0x00);
            REG_B_Write(0x00);
            REG_B_Write(0x00);
            GREEN_Write(ringBuf.buf[ringBuf.tail].packet.drums);
        }
            

        
    } /* END for(;;) */
    
} /* END main() */

