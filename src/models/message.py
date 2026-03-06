from .base import BaseModel


class Message(BaseModel):
    dt: str = None
    metrics: list = None
