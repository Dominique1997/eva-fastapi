import json
from datetime import timedelta

settings = json.load(open("settings.json"))

class Settings:
    @classmethod
    def get_encryption_key(cls):
        return settings["encryption_key"]

    @classmethod
    def get_algorithm(cls):
        return settings["algorithm"]

    @classmethod
    def get_delta_time(cls):
        return timedelta(
            microseconds=settings["login_time_microseconds"],
            milliseconds=settings["login_time_milliseconds"],
            seconds=settings["login_time_seconds"],
            minutes=settings["login_time_minutes"],
            hours=settings["login_time_hours"],
            days=settings["login_time_days"],
            weeks=settings["login_time_weeks"]
        )
