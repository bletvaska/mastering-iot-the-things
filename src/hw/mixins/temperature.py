class TemperatureMixin:
    class Unit:
        IMPERIAL: str = 'imperial'
        STANDARD: str = 'standard'
        METRIC: str = 'metric'

    def temperature(self, units=Unit.METRIC) -> float:
        raise NotImplementedError
