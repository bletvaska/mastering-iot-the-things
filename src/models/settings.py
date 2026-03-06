from models.base import BaseModel


class WiFi(BaseModel):
    ssid: str = None
    password: str = None


class MQTT(BaseModel):
    broker: str = None
    port: int = 1883
    username: str = None
    password: str = None
    insecure: bool = True
    topic_prefix: str = None


class Settings(BaseModel):
    wifi = WiFi()
    mqtt = MQTT()
    device_id: str = None
    name: str = None

    def base_topic(self):
        return f'{self.mqtt.topic_prefix}/{self.device_id}'
