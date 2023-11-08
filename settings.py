import json
from datetime import timedelta


class Settings:
    settings = json.load(open("json_files/settings.json"))

    @classmethod
    def get_encryption_key(cls):
        return cls.settings["encryption_key"]

    @classmethod
    def get_algorithm(cls):
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

    @classmethod
    def get_server_ip(cls):
        return cls.settings["server_ip"]

    @classmethod
    def get_server_port(cls):
        return cls.settings["server_port"]