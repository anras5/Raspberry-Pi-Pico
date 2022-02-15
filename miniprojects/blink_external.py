import machine
import utime

led_internal = machine.Pin(15, machine.Pin.OUT)

while True:
    led_internal.toggle()
    utime.sleep_ms(200)
