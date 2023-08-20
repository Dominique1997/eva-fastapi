import json
import requests
import wolframalpha
from ai import ai

class IntegrationWolframAlpha():
    credential = json.load(open("secrets.json"))["wolframalpha"]["app_id"]
    client = wolframalpha.Client(credential)

    @classmethod
    def perform_check(cls, sentence):
        client_short_answer = cls.client.query(sentence)
        print(f"short answer: {client_short_answer}")
        answer = requests.post(f"http://api.wolframalpha.com/v1/conversation.jsp?appid={cls.credential}&i={sentence}").json()
        if "error" in answer:
            return {"error": "No result is found"}
        ai_answer = ai.check_sentence(answer)
        print(f"rechecked by wolframalpha: {ai_answer}")
        return {"forced_behaviour": False, "answer": answer["result"]}
