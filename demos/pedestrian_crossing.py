from machine import Pin
import time
import _thread


def button_reader_thread():
    global is_button_pressed
    while True:
        if button.value() == 1:
            is_button_pressed = True
        time.sleep(0.01)


red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)
blue = Pin(12, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_DOWN)
is_button_pressed = False

_thread.start_new_thread(button_reader_thread, ())

while True:
    green.value(0)
    yellow.value(1)
    time.sleep(1)
    yellow.value(0)
    red.value(1)
    time.sleep(1.5)
    if is_button_pressed:
        # pedes blue
        blue.value(1)
        # pedes go
        time.sleep(8)
        # blinking
        for _ in range(5):
            blue.value(0)
            time.sleep(0.2)
            blue.value(1)
            time.sleep(0.2)
        blue.value(0)
        is_button_pressed = False

    time.sleep(2)
    red.value(1)
    yellow.value(1)
    time.sleep(1.5)
    red.value(0)
    yellow.value(0)
    green.value(1)
    time.sleep(9)
