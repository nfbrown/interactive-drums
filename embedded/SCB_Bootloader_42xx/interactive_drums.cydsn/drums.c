/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * Credit for ringBuf goes to:
 * http://www.embedded.com/design/embedded/source-code/4419465/rinBufS-zip---Ring-buffer-basics?isCmsPreview=true
 *
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include "drums.h" 
#include <project.h>

const uint16_t pwm_array[16] = {
    0x0010,
    0x0200,
    0x0400,
    0x0700,
    0x0B00,
    0x1200,
    0x1E00,
    0x2800,
    0x3200,
    0x4100,
    0x5000,
    0x6400,
    0x7D00,
    0xA000,
    0xC800,
    0xFF00
};

/*
    This function sets all the elements of the ringBuff to 0
*/
void ringBuf_init(ringBuf_t *_this){
    memset(_this, 0, sizeof (*_this));
}

/*
    This function returns 1 if the ringBuf is empty
*/
uint8_t ringBuf_empty(ringBuf_t * _this){
    return (0 == _this->count);
}

/*
    This funcion returns full if 
*/
uint8_t ringBuf_full(ringBuf_t * _this){
   return (BUFFER_SIZE == _this->count);
}

/*
    This function returns the oldest packet in the ring buffer.
    The function will then remove the packet from the buffer
    If the buffer is empty, the reserved byte will be 1
*/
packet_t ringBuf_get(ringBuf_t * _this){
    packet_t packet;
    if(_this->count > 0){
        packet = _this->buf[_this->tail];
        _this->tail = WRAP(++_this->tail);
        --_this->count;
    }
    else{
        packet.packet.control = EMPTY_ERR;
    }
    
    return packet;
}

/*
    This function returns the oldest packet in the ring buffer.
    If the buffer is empty, the reserved byte will be 1
*/
packet_t ringBuf_peek(ringBuf_t * _this){
    packet_t packet;
    if(_this->count > 0){
        packet = _this->buf[_this->tail];
    }
    else{
        packet.packet.control = EMPTY_ERR;
    }
    
    return packet;
}
       
void ringBuf_put(ringBuf_t *_this, packet_t _packet ){
    if(_this->count < BUFFER_SIZE){
        _this->buf[_this->head] = _packet;
        _this->head = WRAP(++_this->head);
        ++_this->count; 
    }
}
    
void ringBuf_flush(ringBuf_t *_this){
    _this->count    = 0;
    _this->head     = 0;
    _this->tail     = 0;
}

uint8_t set_red_pwm(uint8_t channel, uint8_t drums, uint8_t position_in_queue, uint8_t time_in_packet){
    uint16_t pwmVal = pwm_array[15 - ( (position_in_queue << 2) + time_in_packet) ];
    
    /* Determine how bright the LEDS should be based on their place in the queue */
    
    /* Channel 0 PWM is RED_A - REG_A */
    /* Highest Precedence */
    if(channel & 0x01){
        RED_A_WriteCompare(pwmVal);
        //RED_A_Start();
        REG_A_Write(drums);
        REG_B_Write(REG_B_Read() & ~drums);
        REG_C_Write(REG_C_Read() & ~drums);
        
        return 0x01;
    }
    
    /* Channel 0 PWM is RED_B - REG_B */
    /* Mid Precedence */
    else if (channel & 0x02){
        RED_B_WriteCompare(pwmVal);
        //RED_A_Start();
        REG_B_Write(drums);
        REG_C_Write(REG_C_Read() & ~drums);
        return 0x02;
    }
 
    /* Channel 0 PWM is RED_A - REG_A */
    /* Low Precedence */
    else if(channel & 0x03){
        RED_C_WriteCompare(pwmVal);
        //RED_A_Start();
        REG_C_Write(drums);
        return 0x04;
    }
    
    else{
        return 0xFF;
    }
}

/* [] END OF FILE */