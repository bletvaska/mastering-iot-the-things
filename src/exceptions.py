class THSensorException(Exception):
    pass


class NetworkError(THSensorException):
    pass


class DeviceError(THSensorException):
    pass


class MQTTError(THSensorException):
    pass
