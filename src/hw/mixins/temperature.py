class TemperatureUnit:
    IMPERIAL: str = 'imperial'
    STANDARD: str = 'standard'
    METRIC: str = 'metric'

class TemperatureMixin:
    def temperature(self, units=TemperatureUnit.METRIC) -> float:
        raise NotImplementedError
