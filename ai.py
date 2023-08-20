import json
import nltk
from random import choice
from nltk.corpus import stopwords
nltk.download('stopwords')

class ai():
    intents = json.load(open("intents.json"))["intents"]
    recognize_data = {}
    ignore_stopwords = ["hi", "hello"]


    @classmethod
    def load_intents(cls):
        for intent in cls.intents:
            cls.recognize_data[intent["tag"]] = {}
            cls.recognize_data[intent["tag"]]["pattern_words"] = set()
            cls.recognize_data[intent["tag"]]["responses"] = intent["responses"]
            combined_patterns = ""
            for pattern in intent["patterns"]:
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = set(word for word in str(combined_patterns).split(" ") if word in cls.ignore_stopwords or word not in stopwords.words())
            print(cls.recognize_data[intent["tag"]]["pattern_words"])

    @classmethod
    def check_sentence(cls, sentence):
        for data in cls.recognize_data:
            if len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"]))) > 0:
                return {"forced_behaviour": True, "answer": choice(cls.recognize_data[data]["responses"]), "tag": data}
        return {"error": "No result is found"}
