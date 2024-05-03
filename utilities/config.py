import json
from datetime import timedelta


class Config:
    configFile = json.load(open("./json_files/eva_config.json"))
    default_config = configFile["default"]
    specific_config = configFile["specific"]
    default_settings = default_config["settings"]
    specific_settings = specific_config["settings"]

    @classmethod
    def get_encryption_key(cls):
        server_salt_key = "salt"
        return cls.specific_settings.get(server_salt_key, cls.default_settings.get(server_salt_key, "DitIsDeStandaardSaltKey"))

    @classmethod
    def get_algorithm(cls):
        server_algorithm_key = "algorithm"
        return cls.specific_settings.get(server_algorithm_key, cls.default_settings.get(server_algorithm_key, "HS256"))

    @classmethod
    def get_delta_time(cls):
        login_time_seconds_key = "login_time_seconds"
        login_time_minutes_key = "login_time_minutes"
        login_time_hours_key = "login_time_hours"
        login_time_days_key = "login_time_days"
        login_time_weeks_key = "login_time_weeks"

        return timedelta(
            seconds=cls.specific_settings.get(login_time_seconds_key, cls.default_settings.get(login_time_seconds_key, 1)),
            minutes=cls.specific_settings.get(login_time_minutes_key, cls.default_settings.get(login_time_minutes_key, 1)),
            hours=cls.specific_settings.get(login_time_hours_key, cls.default_settings.get(login_time_hours_key, 1)),
            days=cls.specific_settings.get(login_time_days_key, cls.default_settings.get(login_time_days_key, 1)),
            weeks=cls.specific_settings.get(login_time_weeks_key, cls.default_settings.get(login_time_weeks_key, 1))
        )

    @classmethod
    def get_server_ip(cls):
        server_ip_key = "server_ip"
        return cls.specific_settings.get(server_ip_key, cls.default_settings.get(server_ip_key, "127.0.0.1"))

    @classmethod
    def get_server_port(cls):
        server_port_key = "server_port"
        return cls.specific_settings.get(server_port_key, cls.default_settings.get(server_port_key, 9999))

    @classmethod
    def get_sql_server_ip(cls):
        sql_server_ip_key = "sql_server_ip"
        return cls.specific_settings.get(sql_server_ip_key, cls.default_settings.get(sql_server_ip_key, "127.0.0.1"))

    @classmethod
    def get_sql_server_port(cls):
        sql_server_port_key = "sql_server_port"
        return cls.specific_settings.get(sql_server_port_key, cls.default_settings.get(sql_server_port_key, 3306))

    @classmethod
    def test_mode(cls):
        server_test_mode_key = "test_mode"
        return cls.specific_settings.get(server_test_mode_key, cls.default_settings.get(server_test_mode_key, False))
