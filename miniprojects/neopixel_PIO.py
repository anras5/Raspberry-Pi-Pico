import array, utime
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 10


# There are two stages for data coming in to the state machine. The first is a bit of memory
# called a First In, First Out (or FIFO). This is where our main Python program sends data to. The
# second is the Output Shift Register (OSR). This is where the out() instruction fetches data from.
# The two are linked by pull instructions which take data from the FIFO and put it in the OSR.
# However, since our program is set up with autopull enabled with a threshold of 24, each time
# we’ve read 24 bits from the OSR, it will be reloaded from the FIFO.
# The instruction out(x,1) takes one bit of data from the OSR and places it in a variable called
# x (there are only two available variables in PIO: x and y).
# The jmp instruction tells the code to move directly to a particular label, but it can have a
# condition. The instruction jmp(not_x, "do_zero") tells the code to move to do_zero if the
# value of x is 0 (or, in logical terms, if not_x is true, and not_x is the opposite of x – in PIO-level
# speak, 0 is false and any other number is true).
# There’s a bit of jmp spaghetti that is mostly there to ensure that the timings are consistent
# because the loop has to take exactly the same number of cycles every iteration to keep the
# timing of the protocol in line.
# The one aspect we’ve been ignoring here is the .side() bits. These are similar to set() but
# they take place at the same time as another instruction. This means that out(x,1) takes place
# as .side(0) is setting the value of the sideset pin to 0.
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]


# Create the StateMachine with the ws2812 program, outputting on Pin(0).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# -------------------------------------------------------------------------------------------------------------------- #
# Display a pattern on the LEDs via an array of LED RGB values.

# Here we keep track of an array called ar that holds the data we want our LEDs to have.
# Each number in the array contains the data for all three colours on a single light.
# The format is a little strange as it’s in binary. One thing about working with PIO is that
# you often need to work with individual bits of data. Each bit of data is a 1 or 0,
# and numbers can be built up in this way, so the number 2 in base 10 (as we call
# normal numbers) is 10 in binary. 3 in base 10 is 11 in binary. The largest number in eight bits of
# binary is 11111111, or 255 in base 10.

# To make matters a little more confusing, we’re actually storing three numbers in a single
# number. This is because in MicroPython, whole numbers are stored in 32 bits, but we only need
# eight bits for each number. There’s a little free space at the end as we really only need 24 bits,
# but that’s OK.

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

# This creates an array which has I as the first value, and then a 0 for every LED. The reason
# there’s an I at the start is that it tells MicroPython that we’re using a series of 32-bit values.
# However, we only want 24 bits of this sent to the PIO for each value, so we tell the put command
# to remove eight bits with: 'sm.put(ar, 8)'

print("blue")
for j in range(0, 255):
    for i in range(NUM_LEDS):
        ar[i] = j
    sm.put(ar, 8)
    utime.sleep_ms(10)

print("red")
for j in range(0, 255):
    for i in range(NUM_LEDS):
        ar[i] = j << 8
    sm.put(ar, 8)
    utime.sleep_ms(10)

print("green")
for j in range(0, 255):
    for i in range(NUM_LEDS):
        ar[i] = j << 16
    sm.put(ar, 8)
    utime.sleep_ms(10)

print("white")
for j in range(0, 255):
    for i in range(NUM_LEDS):
        ar[i] = (j << 16) + (j << 8) + j
sm.put(ar, 8)
utime.sleep_ms(10)
