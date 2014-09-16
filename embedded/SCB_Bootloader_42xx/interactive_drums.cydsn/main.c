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

#define RESET 2

void pullPacketInterrupt(void);

ringBuf_t ringBuf;


char string_buffer[50];

CY_ISR_PROTO(beat);
CY_ISR(beat){
    // Do processing for each pacet
    char buf[50];
    sprintf(buf, "%d", timer_ReadCounter());
    UART_UartPutString(buf);
    UART_UartPutCRLF('.');   
    timer_Start();
}

int main()
{
    /*
     *  Variable Decleration
    */
    
    /*
     * Setup Code
    */
    UART_SetCustomInterruptHandler(&pullPacketInterrupt);
    ringBuf_init(&ringBuf);
    UART_Start();
    
    
    // Setup timer ISR
    timer_Start();
    tick_StartEx(beat);
    
    CyGlobalIntEnable; 
    
    for(;;)
    {
//        if(UART_SpiUartGetRxBufferSize()){
//            temp_char = UART_UartGetByte();
//            if((temp_char & 0x0000FF00) == 0){
//                packets[number_of_packets] = (uint8_t) temp_char;
//                number_of_packets ++;
//                
//            }
//            if(number_of_packets > 3){
//                number_of_packets = 0;
//                sprintf(string_buffer, "Packet recieved... %d %d %d %d", packets[0], packets[1], packets[2], packets[3]);
//                UART_UartPutString(string_buffer);
//                UART_UartPutCRLF('.');
//            }    
//        }
        /* Place your application code here. */
    }
}

void pullPacketInterrupt(void){
    uint8_t i;
    packet_t temp_packet;
    
    if(0u != (UART_GetRxInterruptSourceMasked() & UART_INTR_RX_TRIGGER)){
        if(UART_SpiUartGetRxBufferSize() > 3){
            for(i = 0; i < 4; i++){     // Pull in 4 bytes from the UART and save them into a temp packet
                temp_packet.byte[i] = (uint8_t) (UART_UartGetByte() & 0xFF);
            }
        }
        
        // Check to see if the reset code / bit is set in the packet
        if(temp_packet.packet.control == RESET){
            ringBuf_flush(&ringBuf);
        }
        else if(!ringBuf_full(&ringBuf)){
             ringBuf_put(&ringBuf, temp_packet);
        }
        
        UART_ClearRxInterruptSource(UART_INTR_RX_ALL);
    }
}

/* [] END OF FILE */
