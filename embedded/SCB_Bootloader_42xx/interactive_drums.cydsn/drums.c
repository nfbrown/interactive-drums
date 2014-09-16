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
        packet.packet.reserved = 1;
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

/* [] END OF FILE */