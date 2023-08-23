import json
from datetime import timedelta


class Settings:
    settings = json.load(open("settings.json"))

    @classmethod
    def get_encryption_key(cls):
        print(cls.settings["encryption_key"])
        return cls.settings["encryption_key"]

    @classmethod
    def get_algorithm(cls):
        print(cls.settings["algorithm"])
        return cls.settings["algorithm"]

    @classmethod
    def get_delta_time(cls):
        return timedelta(
            seconds=cls.settings["login_time_seconds"],
            minutes=cls.settings["login_time_minutes"],
            hours=cls.settings["login_time_hours"],
            days=cls.settings["login_time_days"],
            weeks=cls.settings["login_time_weeks"]
        )