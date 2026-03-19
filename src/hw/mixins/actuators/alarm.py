EVERY_SECOND = 0
EVERY_MINUTE = 1
EVERY_HOUR = 2
EVERY_DAY = 3
EVERY_WEEK = 4
EVERY_MONTH = 5


class AlarmMixin:
    def set_alarm(self,
                  when: str,
                  day: int | None = None,
                  hour: int | None = None,
                  minute: int | None = None,
                  second: int | None = None,
                  alarm_id: int = 0,
                  ):
        """
        Configure a recurring alarm.

        :param alarm_id: Alarm ID
        :param when: Alarm repeat mode (AlarmRepeat constants).
        :param day: Day of week/month (depending on implementation).
        :param hour: Hour (0–23).
        :param minute: Minute (0–59).
        :param second: Second (0–59).
        :raises NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError()

    def clear_alarm(self, nr: int = 0):
        raise NotImplementedError()
