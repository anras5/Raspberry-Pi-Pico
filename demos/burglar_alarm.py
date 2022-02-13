from machine import Pin
import utime

sensor_pir = Pin(28, Pin.IN, Pin.PULL_DOWN)
led = Pin(15, Pin.OUT)


def pir_handler(pin):
    utime.sleep_ms(100)
    if pin.value():
        for i in range(10):
            led.toggle()
            utime.sleep_ms(100)


sensor_pir.irq(trigger=Pin.IRQ_RISING, handler=pir_handler)