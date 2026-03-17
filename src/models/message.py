from .base import BaseModel, Field


class Message(BaseModel):
    dt: str = Field(default=None, type=str, optional=True)
    metrics: list = Field(default_factory=list)
