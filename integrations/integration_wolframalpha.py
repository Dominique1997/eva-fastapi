import json
import requests
import wolframalpha

class IntegrationWolframAlpha():
    credential = json.load(open("secrets.json"))["wolframalpha"]["app_id"]
    client = wolframalpha.Client(credential)
    @classmethod
    def perform_check(cls, sentence):
        answer = requests.post(f"http://api.wolframalpha.com/v1/conversation.jsp?appid={cls.credential}&i={sentence}").json()
        if "error" in answer:
            return json.dumps({"error": "No result is found"})
        return json.dumps({"forced_behaviour": False, "answer": answer["result"]})
