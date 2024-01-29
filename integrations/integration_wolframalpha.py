import requests
import wolframalpha
from utilities.credentials import Credentials


class IntegrationWolframAlpha():
    appID = Credentials.get_wolframalpha_app_id()
    error_message = "I did not understand your question"
    client = wolframalpha.Client(appID)
    baseUrl = ""

    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/spoken?appid={cls.appID}&i={sentence}").text
        return {"forced_behaviour": False, "answer": answer}
