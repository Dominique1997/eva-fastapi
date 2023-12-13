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
    ignore_stopwords = ["hi", "hello"]
    replace_words = [["vtm go", "vtm_go"], ["disney plus, disney_plus"]]

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
            if "trigger" in intent:
                cls.recognize_data[intent["tag"]]["trigger"] = intent['trigger']
            combined_patterns = ""
            for pattern in intent["patterns"]:
                for replace_word in cls.replace_words:
                    IntegrationLogging.log(f"Checking for replace word: {replace_word[0]}")
                    IntegrationLogging.log(f"{replace_word}: {str(pattern).__contains__(replace_word[0]).__str__()}")
                    if str(pattern).__contains__(replace_word[0]):
                        pattern = str(pattern).replace(replace_word[0], replace_word[1])
                        IntegrationLogging.log(f"Updated pattern: {pattern}")
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = set(word for word in str(combined_patterns).split(" ") if word in cls.ignore_stopwords or word not in stopwords.words())
            IntegrationLogging.log(f'Loaded: {cls.recognize_data[intent["tag"]]["pattern_words"]}')

    @classmethod
    def check_sentence(cls, sentence, received_from=None):
        highest_intersection_value = 0
        highest_intersection_tag = "No result is found"
        highest_pattern_words = []
        IntegrationLogging.log(f'checking {sentence}')
        for replace_word in cls.replace_words:
            IntegrationLogging.log(f"Checking for replace word: {replace_word[0]}")
            IntegrationLogging.log(f"{replace_word}: {str(sentence).__contains__(replace_word[0]).__str__()}")
            if str(sentence).__contains__(replace_word[0]):
                sentence = str(sentence).replace(replace_word[0], replace_word[1])
                IntegrationLogging.log(f"Checking sentence: {sentence}")
        for data in cls.recognize_data:
            if received_from in cls.recognize_data[data]["accessible_by"]:
                set_sentence = set(str(sentence).split(" "))
                if len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"]))) > highest_intersection_value:
                    highest_intersection_value = len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"])))
                    highest_intersection_tag = data
                    highest_pattern_words = cls.recognize_data[data]["pattern_words"]
                    IntegrationLogging.log(f'Intersection found with: {cls.recognize_data[data]["pattern_words"]}')
                if len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"]))) == highest_intersection_value:
                    intersection_amount = highest_intersection_value
                    union_amount_sentence_current_highest = intersection_amount / len(set_sentence.union(highest_pattern_words))
                    union_amount_sentence_two = intersection_amount / len(set_sentence.union(set(cls.recognize_data[data]["pattern_words"])))
                    if union_amount_sentence_two > union_amount_sentence_current_highest:
                        highest_intersection_value = len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"])))
                        highest_intersection_tag = data
                        highest_pattern_words = cls.recognize_data[data]["pattern_words"]
        if highest_intersection_value != 0:
            if "trigger" in cls.recognize_data[highest_intersection_tag]:
                if cls.recognize_data[highest_intersection_tag]["trigger"] == "home-assistant":
                    cls.integration_home_assistant.check_tag(highest_intersection_tag)
            return {"forced_behaviour": True, "answer": choice(cls.recognize_data[highest_intersection_tag]["responses"]), "tag": highest_intersection_tag}
        IntegrationLogging.log(f'No intersection found')
        return {"error": "No result is found"}

