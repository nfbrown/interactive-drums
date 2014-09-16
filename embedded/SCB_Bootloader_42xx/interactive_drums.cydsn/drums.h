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
    #define WRAP(x) ((x) %  BUFFER_SIZE)
    
    typedef union {
    	struct {
    		uint32_t drums:16;
            uint32_t speed:8;
            uint32_t reserved:1;
            uint32_t control:4;
            uint32_t reset:1;
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
    void        ringBuf_put(ringBuf_t *_this, packet_t _packet);
    void        ringBuf_flush(ringBuf_t *_this);
    
#endif
    
/* [] END OF FILE */