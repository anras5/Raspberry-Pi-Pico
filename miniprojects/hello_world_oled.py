from oled_display.oled_spi import OLED_2inch23

oled = OLED_2inch23()
oled.fill(0x0000)
oled.text("Hello world", 1, 2, oled.white)
oled.show()
