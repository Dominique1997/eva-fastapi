import json
import nltk
from random import choice
from nltk.corpus import stopwords
from integrations.integration_home_assistant import IntegrationHomeAssistant
from integrations.integration_logging import IntegrationLogging
nltk.download('stopwords')


class IntegrationAi:
    intents = json.load(open("json_files/intents.json"))["intents"]
    integration_home_assistant = IntegrationHomeAssistant
    recognize_data = {}
    ignore_stopwords = ["hi", "hello", "plus"]

    @classmethod
    def load_intents(cls):
        IntegrationLogging.log("loading homeassistant information")
        cls.integration_home_assistant.load_information()
        IntegrationLogging.log("Loading intents")
        for intent in cls.intents:
            cls.recognize_data[intent["tag"]] = {}
            cls.recognize_data[intent["tag"]]["pattern_words"] = set()
            cls.recognize_data[intent["tag"]]["responses"] = intent["responses"]
            cls.recognize_data[intent["tag"]]["accessible_by"] = intent['accessible_by']
            combined_patterns = ""
            for pattern in intent["patterns"]:
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = set(word for word in str(combined_patterns).split(" ") if word in cls.ignore_stopwords or word not in stopwords.words())
            IntegrationLogging.log(f'Loaded: {cls.recognize_data[intent["tag"]]["pattern_words"]}')

    @classmethod
    def check_sentence(cls, sentence, received_from=None):
        highest_intersection_value = 0
        highest_intersection_tag = "No result is found"
        IntegrationLogging.log(f'checking {sentence}')
        for data in cls.recognize_data:
            if received_from in cls.recognize_data[data]["accessible_by"]:
                if len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"]))) > 0:
                    if len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"]))) > highest_intersection_value:
                        highest_intersection_value = len(set(str(sentence).split(" ")).intersection(set(cls.recognize_data[data]["pattern_words"])))
                        highest_intersection_tag = data
                        print(highest_intersection_value, data)
                    IntegrationLogging.log(f'Intersection found with: {cls.recognize_data[data]["pattern_words"]}')
        if highest_intersection_value != 0:
            cls.integration_home_assistant.check_tag(highest_intersection_tag)
            return {"forced_behaviour": True, "answer": choice(cls.recognize_data[data]["responses"]), "tag": data}
        IntegrationLogging.log(f'No intersection found')
        return {"error": "No result is found"}

