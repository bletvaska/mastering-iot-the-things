from models.base import BaseModel, Field


class WiFi(BaseModel):
    ssid: str = Field(default=None, type=str, optional=True)
    password: str = Field(default=None, type=str, optional=True)


class MQTT(BaseModel):
    broker: str = Field(default=None, type=str, optional=True)
    port: int = 1883
    username: str = Field(default=None, type=str, optional=True)
    password: str = Field(default=None, type=str, optional=True)
    insecure: bool = True
    topic_prefix: str = Field(default=None, type=str, optional=True)


class Admin(BaseModel):
    username: str = Field(default=None, type=str)
    password: str = Field(default=None, type=str)


class Settings(BaseModel):
    wifi: WiFi = Field(default_factory=WiFi, type=WiFi)
    mqtt: MQTT = Field(default_factory=MQTT, type=MQTT)
    admin: Admin = Field(default_factory=Admin, type=Admin)
    device_id: str = Field(default=None, type=str, optional=True)
    name: str = Field(default=None, type=str, optional=True)

    def base_topic(self):
        return f'{self.mqtt.topic_prefix}/{self.device_id}'
