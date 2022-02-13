from machine import Pin, ADC
import utime

sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    print(temperature)
    utime.sleep(2)
