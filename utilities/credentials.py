import json
import os

class Credentials():
    credentials_list = json.load(open(f"{os.getcwd()}/json_files/secrets.json"))

    @classmethod
    def get_wolframalpha_app_id(cls):
        return cls.credentials_list["wolframalpha"]

    @classmethod
    def get_home_assistant_token(cls):
        return cls.credentials_list["home_assistant_token"]

    @classmethod
    def get_calendarific_token(cls):
        return cls.credentials_list["calendarific"]

    @classmethod
    def get_omdb_token(cls):
        return cls.credentials_list["omdb"]

    @classmethod
    def get_audiodb_token(cls):
        return cls.credentials_list["audiodb"]