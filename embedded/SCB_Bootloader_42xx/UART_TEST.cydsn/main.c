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



int main()
{
    //char test_string[] = "HELLO WORLD \r\n";
    char temp_char = 'A';
    /* Place your initialization/startup code here (e.g. MyInst_Start()) */
    UART_Start();
    
    /* CyGlobalIntEnable; */ /* Uncomment this line to enable global interrupts. */
    for(;;)
    {
        temp_char = UART_UartGetChar() + 1;
        if (temp_char != 1){
            UART_UartPutChar(temp_char);     
        }
            
        
    }
}

/* [] END OF FILE */
