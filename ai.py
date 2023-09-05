import json
import nltk
import difflib
from random import choice
from utilities import Utilities
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

    @classmethod
    def check_sentence(cls, sentence):
        for data in cls.recognize_data:
            print(data, set(str(sentence).split(" ")), set(cls.recognize_data[data]["pattern_words"]))
            print(round(cls.average_similarity(set(str(sentence).split(" ")), set(cls.recognize_data[data]["pattern_words"])), 2))
            if len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"]))) > 0:
                return {"forced_behaviour": True, "answer": choice(cls.recognize_data[data]["responses"]), "tag": data}
        return {"error": "No result is found"}

    @classmethod
    def average_similarity(cls, input_sentence, compare_sentence):
        total_similarity = 0
        total_pairs = 0
        highest_similarity = 0
        highest_similar_sentence = ""

        for input_sentence_word in input_sentence:
            for compare_sentence_word in compare_sentence:
                total_similarity += difflib.SequenceMatcher(None, input_sentence_word, compare_sentence_word).ratio()
                if total_similarity > highest_similarity:
                    highest_similar_sentence = compare_sentence
                    print(highest_similar_sentence)
                total_pairs += 1

        return total_similarity / total_pairs * 100 if total_pairs != 0 else 0
