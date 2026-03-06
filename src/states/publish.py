import json
import os
from machine import RTC

from states.ota import OTA
from constants import METRICS_FILE
from models.message import Message
from models.metric import Metric
from .base import BaseState
from helpers import to_iso8601


class Publish(BaseState):
    name = "Publish"

    def enter(self) -> None:
        super().enter()
        self.metrics = []

        with open(METRICS_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(';')

                temperature = Metric(
                    dt=parts[0],
                    name='temperature',
                    value=float(parts[1]),
                    units=parts[2]
                )
                self.metrics.append(temperature)

                humidity = Metric(
                    dt=parts[0],
                    name='humidity',
                    value=float(parts[3]),
                    units='%'
                )
                self.metrics.append(humidity)

    def exec(self):
        message = Message(
            dt=to_iso8601(RTC().datetime()),
            metrics=self.metrics
        )

        topic = f'{self.context.settings.base_topic()}/data'
        self.context.mqtt_client.publish(topic, json.dumps(message.model_dump()))

        return OTA(self.context)

    def exit(self) -> None:
        super().exit()
        os.unlink(METRICS_FILE)
