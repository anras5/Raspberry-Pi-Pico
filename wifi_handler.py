from machine import UART
import utime
import json

# load wifi ssid, wifi password, Ubidots API token and password from a secret file
with open("env/env.json") as f:
    private_variables = json.load(f)

wifi_ssid = private_variables['wifi_ssid']
wifi_password = private_variables['wifi_password']
ubidots_token = private_variables['ubidots_token']
device_label = "raspberry-pi-pico-bme"
user_agent = private_variables['user_agent']


class WifiHandler:

    def __init__(self):
        self.uart = UART(0, 115200)
        self.lst = []

    def _send_command(self, command, ack, timeout=20000):
        self.uart.write(command + '\r\n')
        t = utime.ticks_ms()
        while (utime.ticks_ms() - t) < timeout:
            s = self.uart.read()
            if s is not None:
                s = s.decode()
                self.lst.append(s)
                print(s)

                if s.find(ack) >= 0:
                    return True
        return False

    def wifi_connect(self):
        self._send_command("AT", "OK")
        self._send_command("AT+CWMODE=3", "OK")
        self._send_command(f'AT+CWJAP="{wifi_ssid}","{wifi_password}"', "OK", 20000)
        self._send_command("AT+CIFSR", "OK")
        self._send_command("AT+CIPSEND", ">")

    def send_tcp(self, variables: dict):
        send = 'AT+CIPSTART="TCP","industrial.api.ubidots.com",9012'
        self.uart.write(send + '\r\n')
        utime.sleep(2)

        # build payload and find its length
        payload = f'{device_label}=>'
        for variable_label, value in variables.items():
            payload += f'{variable_label}:{value},'
        payload = payload[:-1]
        payload_length = len(payload)

        # find request length
        req_length = 11
        req_length += len(user_agent + ubidots_token + str(payload_length) + payload)

        send = f"AT+CIPSEND={req_length}"
        self.uart.write(send + '\r\n')
        utime.sleep(0.6)

        send = f'{user_agent}|POST|{ubidots_token}|{payload}|end'
        self.uart.write(send + '\r\n')
        utime.sleep(0.6)

        print("Data sent: " + payload)
