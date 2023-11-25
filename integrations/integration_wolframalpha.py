import requests
import wolframalpha
from integrations.integration_ai import IntegrationAi as ai
from credentials import Credentials


class IntegrationWolframAlpha():
    appID = Credentials.get_wolframalpha_app_id()
    error_message = "Wolfram Alpha did not understand your input"
    client = wolframalpha.Client(appID)

    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/spoken?appid={cls.appID}&i={sentence}").text
        if answer != cls.error_message:
            ai.check_sentence(answer)
        return {"forced_behaviour": False, "answer": answer}
