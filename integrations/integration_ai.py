import json
import nltk
from random import choice
from nltk.corpus import stopwords

nltk.download('stopwords')

class IntegrationAi():
    intents = json.load(open("json_files/intents.json"))["intents"]
    recognize_data = {}
    ignore_stopwords = ["hi", "hello"]


    @classmethod
    def load_intents(cls):
        for intent in cls.intents:
            cls.recognize_data[intent["tag"]] = {}
            cls.recognize_data[intent["tag"]]["pattern_words"] = set()
            cls.recognize_data[intent["tag"]]["responses"] = intent["responses"]
            cls.recognize_data[intent["tag"]]["accessible_by"] = intent['accessible_by']
            combined_patterns = ""
            for pattern in intent["patterns"]:
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = set(word for word in str(combined_patterns).split(" ") if word in cls.ignore_stopwords or word not in stopwords.words())

    @classmethod
    def check_sentence(cls, sentence, received_from=None):
        for data in cls.recognize_data:
            if received_from in cls.recognize_data[data]["accessible_by"]:
                if len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"]))) > 0:
                    return {"forced_behaviour": True, "answer": choice(cls.recognize_data[data]["responses"]), "tag": data}
        return {"error": "No result is found"}

