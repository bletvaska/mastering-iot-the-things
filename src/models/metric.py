from .base import BaseModel


class Metric(BaseModel):
    dt: str = None
    name: str = None
    value: float = None
    units: str = None
