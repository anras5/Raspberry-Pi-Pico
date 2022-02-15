from oled_display.oled_spi import OLED_2inch23
from hcsr04 import HCSR04
import utime

oled = OLED_2inch23()

sensor = HCSR04(trigger_pin=21, echo_pin=20)

while True:
    distance = sensor.distance_cm()
    oled.fill(oled.black)
    oled.text(f"Distance: {distance:.1f}cm", 0, 12, oled.white)
    oled.show()
    utime.sleep_ms(300)