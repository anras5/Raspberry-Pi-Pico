from machine import Pin
import utime

trigger = Pin(14, Pin.OUT)
echo = Pin(13, Pin.IN)

while True:
    trigger.low()
    utime.sleep_us(5)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signal_off = utime.ticks_us()
    while echo.value() == 1:
        signal_on = utime.ticks_us()
    distance = ((signal_on - signal_off) * 0.0343) / 2
    print(f"The distance from object is {distance}cm")
    utime.sleep(1)
