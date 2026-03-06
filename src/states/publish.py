import json

import os
from machine import RTC

from helpers import to_iso8601

from constants import METRICS_FILE
from models.message import Message
from models.metric import Metric
from .sleep import Sleep
from .base import BaseState


class Publish(BaseState):
    name = "Publish"

    def exec(self):
        metrics = []

        with open(METRICS_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(';')
                temperature = Metric(
                    dt=parts[0],
                    name='temperature',
                    value=float(parts[1]),
                    units=parts[2]
                )
                metrics.append(temperature)

                humidity = Metric(
                    dt=parts[0],
                    name='humidity',
                    value=float(parts[3]),
                    units='%'
                )
                metrics.append(humidity)

        message = Message(
            dt=to_iso8601(RTC().datetime()),
            metrics=metrics
        )

        topic = f'{self.context.settings.base_topic()}/data'
        self.context.mqtt_client.publish(topic, json.dumps(message.model_dump()))

        os.unlink(METRICS_FILE)

        return Sleep(self.context)
