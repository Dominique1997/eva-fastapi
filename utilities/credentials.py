import json
import os

class Credentials():
    print(os.getcwd())
    credentials_list = json.load(open(f"{os.getcwd()}/json_files/secrets.json"))
    @classmethod
    def get_wolframalpha_app_id(cls):
        return cls.credentials_list["wolframalpha"]

    @classmethod
    def get_home_assistant_token(cls):
        return cls.credentials_list["home_assistant_token"]