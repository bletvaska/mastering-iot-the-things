from models.base import BaseModel


class WiFi(BaseModel):
    ssid: str = None
    password: str = None


class Settings(BaseModel):
    wifi = WiFi()
