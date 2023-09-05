import json
import requests
from ai import ai
import wolframalpha


class IntegrationWolframAlpha():
    appID = json.load(open("secrets.json"))["wolframalpha"]["app_id"]
    error_message = "Wolfram Alpha did not understand your input"
    client = wolframalpha.Client(appID)

    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/spoken?appid={cls.appID}&i={sentence}").text
        if answer != cls.error_message:
            ai.check_sentence(answer)
        return {"forced_behaviour": False, "answer": answer}
