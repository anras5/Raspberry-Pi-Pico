import random
from machine import Pin
import time


def button_handler(pin):
    global pressed
    if not pressed:
        pressed = True
        timer_reaction = time.ticks_diff(time.ticks_ms(), timer_start)
        print(f"Your reaction time was {timer_reaction} milliseconds!")
        global fastest_button
        fastest_button = pin


led = Pin(15, Pin.OUT)
button1 = Pin(13, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
pressed = False
fastest_button = None

led.value(1)
time.sleep(random.uniform(5, 10))
led.value(0)
timer_start = time.ticks_ms()
button1.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
button2.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


while fastest_button is None:
    time.sleep(1)
    if fastest_button is button1:
        print("Right Player wins!")
    elif fastest_button is button2:
        print("Left Player wins!")
