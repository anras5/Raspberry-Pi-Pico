from machine import Pin

led_external = Pin(14, Pin.OUT)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value() == 1:
        led_external.value(1)
    else:
        led_external.value(0)
