import asyncio

import aioble

from constants import METRICS_FILE
from lib.bthome import BTHome
from .base import BaseState
from .connect_network import ConnectNetwork


class Advertisement(BaseState):
    name = 'Advertisement'

    def enter(self):
        last_measurement = None

        with open(METRICS_FILE, 'r') as file:
            for line in file:
                last_measurement = line

        dt, temp, temp_unit, hum = last_measurement.strip().split(';')
        self.measurement = {
            'dt': dt,
            'temp': float(temp),
            'temp_unit': temp_unit,
            'hum': float(hum)
        }

    async def exec(self):
        beacon = BTHome('THS-mirek')
        beacon.temperature = self.measurement['temp']
        beacon.humidity = self.measurement['hum']

        print(self.measurement['temp'], self.measurement['hum'])

        advert = beacon.pack_advertisement(
            BTHome.TEMPERATURE_SINT16_X100,
            BTHome.HUMIDITY_UINT16_X100
        )

        asyncio.run(self._advertise(advert))
        # async with await aioble.advertise(
        #         interval_us=250_000,
        #         adv_data=advert,
        #         connectable=False
        # ) as connection:
        #     print(connection)


        return ConnectNetwork(self.context)

    async def _advertise(self, advert):
        try:
            await aioble.advertise(
                interval_us=250_000,
                adv_data=advert,
                connectable=True,
                timeout_ms=5_000,
            )
        except asyncio.TimeoutError as ex:
            print('...BLE Advertise Timeout')
