import utime
from machine import Pin, I2C

import wifi_handler
from oled_display.oled_spi import OLED_2inch23
from environmentSensor.BME280 import BME280 # pressure, temp, hum
from environmentSensor.ICM20948 import ICM20948 # accelerometer
from environmentSensor.LTR390 import LTR390 # UV
from environmentSensor.SGP40 import SGP40
from environmentSensor.TSL2591 import TSL2591

data_sender = wifi_handler.WifiHandler()
screen = OLED_2inch23()
screen.fill(screen.black)
screen.text(f'Connecting to wifi', 1, 12, screen.white)
screen.show()

data_sender.wifi_connect()


i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)
print("=============================")
print("Environment Sensors:")
print("bme280 T&H I2C address:0X76")
devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:', len(devices))

bme280 = BME280()
bme280.get_calib_param()

screen.fill(screen.black)
screen.text(f'Setup done', 1, 12, screen.white)
screen.show()

try:
    while True:
        pressure = round(bme280.readData()[0], 2)
        temperature = round(bme280.readData()[1], 2)
        humidity = round(bme280.readData()[2], 2)

        screen.fill(screen.black)
        screen.text(f'Pressure: {pressure}', 1, 2, screen.white)
        screen.text(f'Temp:     {temperature}', 1, 12, screen.white)
        screen.text(f'Humidity: {humidity}', 1, 22, screen.white)
        screen.text(f'Humidity:', 1, 22, screen.white)
        screen.show()

        variables = {
            'pressure': pressure,
            'temperature': temperature,
            'humidity': humidity
        }

        data_sender.send_tcp(variables)
        utime.sleep(5*60)
except KeyboardInterrupt:
    print("Keyboard Interrupt")
