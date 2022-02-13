from machine import Pin, ADC
import utime

potentiometer = ADC(26)
conversion_factor = 3.3 / 65535

while True:
    print(potentiometer.read_u16() * conversion_factor)
    utime.sleep(2)
