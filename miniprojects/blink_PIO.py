# There are three methods here that all look a little strange, but that set the on-board LED to
# quarter, half, and full brightness. The reason they look a little strange is because they’re written
# in a special language for the PIO system of Pico. You can probably guess what they do –
# flick the LED on and off very quickly in a similar way to how we used PWM. The instruction
# set(pins, 0) turns a GPIO pin off and set(pins, 1) turns the GPIO pin on.


from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import utime


# Each of the three methods has a descriptor above it that tells MicroPython to treat it as a PIO
# program and not a normal method. These descriptors can also take parameters that influence
# the behaviour of the programs. In these cases, we’ve used the set_init parameter to tell the
# PIO whether or not the GPIO pin should start off being low or high.

# Each of these methods – which are really mini programs that run on the PIO state machines –
# loops continuously. So, for example, led_half_brightness will constantly turn the LED on and
# off so that it spends half its time off and half its time on. led_full_brightness will similarly
# loop, but since the only instruction is to turn the LED on, this doesn’t actually change anything.

# The slightly unusual one here is led_quarter_brightness. Each PIO instruction takes
# exactly one clock cycle to run (the length of a clock cycle can be changed by setting the
# frequency, as we’ll see later). However, we can add a number between 1 and 31 in square
# brackets after an instruction, and this tells the PIO state machine to pause by this number of
# clock cycles before running the next instruction. In led_quarter_brightness, then, the two
# set instructions each take one clock cycle, and the delay takes two clock cycles, so the total
# loop takes four clock cycles. In the first line, the set instruction takes one cycle and the delay
# takes two, so the GPIO pin is off for three of these four cycles. This makes the LED a quarter as
# bright as if it were on constantly.
@asm_pio(set_init=PIO.OUT_LOW)
def led_quarter_brightness():
    set(pins, 0)[2]
    set(pins, 1)


@asm_pio(set_init=PIO.OUT_LOW)
def led_half_brightness():
    set(pins, 0)
    set(pins, 1)


@asm_pio(set_init=PIO.OUT_HIGH)
def led_full_brightness():
    set(pins, 1)


# Once you’ve got your PIO program, you need to load it into a state machine. Since we have
# three programs, we need to load them into three state machines (there are eight you can use,
# numbered 0–7)

# The parameters here are:
# The state machine number
# The PIO program to load
# The frequency (which must be between 2000 and 125000000)
# The GPIO pin that the state machine manipulates
sm1 = StateMachine(1, led_quarter_brightness, freq=10000, set_base=Pin(25))
sm2 = StateMachine(2, led_half_brightness, freq=10000, set_base=Pin(25))
sm3 = StateMachine(3, led_full_brightness, freq=10000, set_base=Pin(25))

# In our loop, we cycle through the three different state machines.
while True:
    sm1.active(1)
    utime.sleep(1)
    sm1.active(0)

    sm2.active(1)
    utime.sleep(1)
    sm2.active(0)

    sm3.active(1)
    utime.sleep(1)
    sm3.active(0)