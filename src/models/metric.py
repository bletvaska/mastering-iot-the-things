from .base import BaseModel, Field


class Metric(BaseModel):
    dt: str = Field(default=None, type=str, optional=True)
    name: str = Field(default=None, type=str, optional=True)
    value: float = Field(default=None, type=float, optional=True)
    units: str = Field(default=None, type=str, optional=True)
