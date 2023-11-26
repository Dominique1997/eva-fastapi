import requests
import wolframalpha
from integrations.integration_ai import IntegrationAi as ai
from utilities.credentials import Credentials
from integrations.integration_logging import IntegrationLogging


class IntegrationWolframAlpha():
    appID = Credentials.get_wolframalpha_app_id()
    error_message = "Wolfram Alpha did not understand your input"
    client = wolframalpha.Client(appID)

    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/spoken?appid={cls.appID}&i={sentence}").text
        return {"forced_behaviour": False, "answer": answer}
