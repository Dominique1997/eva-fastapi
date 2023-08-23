import json
import requests
import wolframalpha
from ai import ai

class IntegrationWolframAlpha():
    appID = json.load(open("secrets.json"))["wolframalpha"]["app_id"]
    client = wolframalpha.Client(appID)

    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/spoken?appid={cls.appID}&i={sentence}").text
        return {"forced_behaviour": False, "answer": answer}
