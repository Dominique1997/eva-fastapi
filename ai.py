import json
import nltk
from random import choice
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

class ai():
    intents = json.load(open("intents.json"))["intents"]
    recognize_data = {}

    @classmethod
    def load_intents(cls):
        for intent in cls.intents:
            cls.recognize_data[intent["tag"]] = {}
            cls.recognize_data[intent["tag"]]["pattern_words"] = set()
            cls.recognize_data[intent["tag"]]["responses"] = intent["responses"]
            combined_patterns = " "
            for pattern in intent["patterns"]:
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = [word for word in set(str(combined_patterns).split(" ")) if word not in stopwords.words()]

    @classmethod
    def check_sentence(cls, sentence):
        for data in cls.recognize_data:
            if len(set(str(sentence).split(" ")).intersection(cls.recognize_data[data]["pattern_words"])) > 0:
                return json.dumps({"forced_behaviour": True, "answer": choice(cls.recognize_data[data]["responses"]), "tag": data})
