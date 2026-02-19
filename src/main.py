from machine import Pin
from dht import DHT11
import requests
import json
from time import sleep

from thsensor import THSensor

from constants import DHT_PIN
from helpers import do_connect, get_settings

# settings = get_settings()
# dht = DHT11(Pin(DHT_PIN, Pin.IN))
# do_connect(settings.wifi.ssid, settings.wifi.password)
#
# while True:
#     dht.measure()
#     print(dht.temperature(), dht.humidity())
#
#     url = 'https://webhook.site/7a61f5a8-5e88-47d8-96dd-6abf75a547b2'
#     data = {
#         'teplota': dht.temperature(),
#         'vlhkost': dht.humidity(),
#         "name": "mirek"
#     }
#     response = requests.post(url, data=json.dumps(data))
#     response.close()
#
#     sleep(10)


thsensor = THSensor()
thsensor.run()