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



void pullPacketInterrupt(void);

ringBuf_t ringBuf;
volatile state_t state = BUF_LOAD_S;       //initialze state to waiting for buffer to get full

char string_buffer[50];


uint16_t timer_period = 3200;
extern const uint16_t pwm_array[16];

CY_ISR_PROTO(beat_interrupt);
CY_ISR(beat_interrupt){
    uint8_t i;
    packet_t temp_packet;
    
    switch(state){
        case BUF_LOAD_S:
            // Wait for packets to fill up the buffer
        break;
        
        case LEAD_MODE_S:
            //Fall Through
        
        case WAIT_MODE_S:
            temp_packet = ringBuf_get(&ringBuf);
            if(temp_packet.packet.control != EMPTY_ERR){
                for(i = 0; i < 4; i++)
                    UART_UartPutChar(temp_packet.byte[i]);
            }
//            if(ringBuf.count < 2){
//                state = BUF_LOAD_S;
//            }
        break;
            
        default:
        break;
    }
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
            for(i = 0; i < 4; i++){     // Pull in 4 bytes from the UART and save them into a temp packet
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

int main()
{
    /*
     *  Variable Decleration
    */
    int16_t i;
    uint16_t drumsA, drumsB;
    
    uint8_t freePwm;
    uint8_t time_in_packet, last_time_in_packetS;
    
    /*
     * Setup Code
    */
    UART_SetCustomInterruptHandler(&pullPacketInterrupt);
    ringBuf_init(&ringBuf);
    UART_Start();
    
    // Setup timer ISR
    
    RED_A_Start();
    RED_B_Start();
    RED_C_Start();
    //REG_A_Write(0x00);
    //REG_B_Write(0x00);
    //REG_C_Write(0x00);
    
    timer_Start();
    timer_WritePeriod(3200); // Defaults to 150BPM, 600PPM, 10PPS, 3200 Ticks Per Packet 
    tick_StartEx(beat_interrupt);
    
    CyGlobalIntEnable; 
    
    for(;;)
    {
        /* Start by looking through future packets to set the red leds */
       //if((state == LEAD_MODE) || (state == WAIT_MODE)){
            time_in_packet = timer_ReadCounter() / (timer_period / 4);
            if(time_in_packet != last_time_in_packetS){
                freePwm = 0x07;
                REG_A_Write(0x00);
                REG_B_Write(0x00);
                REG_C_Write(0x00);
                for(i = MAX_PACKET_PARSE ; i > 0; i--){
                    drumsA = ringBuf.buf[WRAP(ringBuf.tail + i)].packet.drums;
                    freePwm &= ~set_red_pwm(freePwm, (uint8_t) drumsA, i, time_in_packet);
                    
                }
                
                last_time_in_packetS = time_in_packet;
            }
            GREEN_Write(ringBuf.buf[ringBuf.tail].packet.drums);
    }
}



/* [] END OF FILE */
