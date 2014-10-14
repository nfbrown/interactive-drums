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
#ifndef STDINT
        #define STDINT
        #include <stdint.h>
#endif

#ifndef STRING
       #define STRING
       #include <string.h>
#endif


#ifndef _DRUMS_H
    #define _DRUMS_H
  
    #define BUFFER_SIZE 16
    #define MIN_BUF     12
    #define WRAP(x) ((x) %  BUFFER_SIZE)
    
    /* defines for the control bit codes */
    #define EMPTY       0
    #define RESET       1
    #define PAUSE       2
    #define PLAY        3
    #define WAIT_MODE   4
    #define LEAD_MODE   5
    #define EMPTY_ERR   6
    #define SEQ_ERR     7
    #define BUFF_LOAD   8
    #define SHOW_MODE   9
    
    
    #define MAX_PACKET_PARSE    3 
    
    /* enum for the various states */
    typedef enum {
        LEAD_MODE_S,
        WAIT_MODE_S,
        SHOW_MODE_S,
        PAUSE_S,
        RESET_S,
        BUF_LOAD_S
    }state_t;
        
    
    typedef union {
    	struct {
    		uint32_t drums:16;
            uint32_t speed:8;
            uint32_t control:6;
            uint32_t sequence:2;
        } packet;
        uint8_t byte[4];
    } packet_t;

    typedef struct ringBuf_t
    {
        packet_t buf[BUFFER_SIZE];
        volatile uint8_t head;
        volatile uint8_t tail;
        volatile uint8_t count;
    } ringBuf_t;
    

    
    void        ringBuf_init(ringBuf_t *_this);
    uint8_t     ringBuf_empty(ringBuf_t *_this);
    uint8_t     ringBuf_full(ringBuf_t *_this);
    packet_t    ringBuf_get(ringBuf_t *_this);
    packet_t    ringBuf_peek(ringBuf_t *_this);
    void        ringBuf_put(ringBuf_t *_this, packet_t _packet);
    void        ringBuf_flush(ringBuf_t *_this);
    uint8_t     set_red_pwm(uint8_t channel, uint8_t drums, uint8_t position_in_queue, uint8_t time_in_packet);
    
#endif
    
/* [] END OF FILE */