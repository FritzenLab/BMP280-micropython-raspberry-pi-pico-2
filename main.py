# Based on code from https://github.com/dafvid/micropython-bmp280/tree/master
from machine import I2C, Pin, Timer
from bmp280 import *
import time

bus = I2C(0)
bmp = BMP280(bus)

button = Pin(14,Pin.IN) #Pi Pico 2
#button = Pin(26,Pin.IN,Pin.PULL_UP) #Xiao RP2350
led= machine.Pin(15, machine.Pin.OUT) #Pi Pico 2
#led= machine.Pin(27, machine.Pin.OUT) #Xiao RP2350

readbmp= 0
buttontime= time.ticks_ms()


bmp.use_case(BMP280_CASE_INDOOR)
bmp.oversample(BMP280_OS_ULTRALOW)

bmp.temp_os = BMP280_TEMP_OS_SKIP
bmp.press_os = BMP280_PRES_OS_SKIP

def myFunction(button):
    global readbmp
    global buttontime
    
    #led.value(not led.value())
    
    if time.ticks_diff(time.ticks_ms(), buttontime) > 500: # this IF will be true every 5	00 ms
        buttontime= time.ticks_ms() #update with the "current" time
        
        print("Interrupt has occurred")
        
        if readbmp == 0: # alternate between reading BMP280 and not reading, for every button press
            readbmp = 1
        else:
            readbmp = 0

        led.value(not led.value())
        
"""
bmp.standby = BMP280_STANDBY_250
bmp.iir = BMP280_IIR_FILTER_2

bmp.spi3w = BMP280_SPI3W_ON

bmp.power_mode = BMP280_POWER_FORCED
# or 
bmp.force_measure()

bmp.power_mode = BMP280_POWER_NORMAL
# or 
bmp.normal_measure()
# also
bmp.in_normal_mode()

bmp.power_mode = BMP280_POWER_SLEEP
# or 
bmp.sleep()"""

if __name__ == "__main__":
    
    initialtime= time.ticks_ms() #https://docs.micropython.org/en/latest/library/time.html
    
    while True:
        button.irq(trigger=Pin.IRQ_RISING, handler=myFunction)
        
        
        if time.ticks_diff(time.ticks_ms(), initialtime) > 2000: # this IF will be true every 1000 ms
            initialtime= time.ticks_ms() #update with the "current" time
            
            #led.value(not led.value())
            
            if readbmp == 1:
            
                print(bmp.temperature)
                print(bmp.pressure)
                
                readbmp= 0

                #True while measuring
                #bmp.is_measuring

            #True while copying data to registers
            #bmp.is_updating