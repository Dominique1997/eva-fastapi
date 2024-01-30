import json
import nltk
from random import choice
from nltk.corpus import stopwords
from integrations.integration_home_assistant import IntegrationHomeAssistant
from integrations.integration_thecocktaildb import IntegrationTheCocktailDB
from integrations.integration_themealdb import IntegrationTheMealDB
from integrations.integration_calendarific import IntegrationCalendarific
from integrations.integration_omdb import IntegrationOMDB
from integrations.integration_theaudiodb import IntegrationTheAudioDB


#TO BE INTEGRATED STILL

#code needs to be fixed
#from integrations.integration_tvdb import IntegrationTVDB
#from integrations.integration_openmeteo import IntegrationOpenMeteo
#from integrations.integration_pokemon import IntegrationPokemon

#recheck needed
#from integrations.integration_openlibrary import IntegrationOpenLibrary


nltk.download('stopwords')


class IntegrationAi:
    intents = json.load(open("json_files/intents.json"))["intents"]
    recognize_data = {}
    ignore_stopwords = ["hi", "hello"]
    replace_words = [["vtm go", "vtm_go"], ["disney plus, disney_plus"]]

    @classmethod
    def load_intents(cls):
        IntegrationHomeAssistant.load_information()
        for intent in cls.intents:
            cls.recognize_data[intent["tag"]] = {}
            cls.recognize_data[intent["tag"]]["pattern_words"] = set()
            cls.recognize_data[intent["tag"]]["responses"] = intent["responses"]
            cls.recognize_data[intent["tag"]]["accessible_by"] = intent['accessible_by']
            if "failure_response" in intent:
                cls.recognize_data[intent["tag"]]["failure_response"] = intent["failure_response"]
            if "trigger" in intent:
                cls.recognize_data[intent["tag"]]["trigger"] = intent['trigger']
            combined_patterns = ""
            for pattern in intent["patterns"]:
                for replace_word in cls.replace_words:
                    if str(pattern).__contains__(replace_word[0]):
                        pattern = str(pattern).replace(replace_word[0], replace_word[1])
                combined_patterns += pattern + " "
            cls.recognize_data[intent["tag"]]["pattern_words"] = set(word for word in str(combined_patterns).split(" "))
            #if word in cls.ignore_stopwords or word not in stopwords.words()
    @classmethod
    def check_sentence(cls, sentence, received_from=None):
        highest_intersection_value = 0
        highest_intersection_tag = "No result is found"
        highest_pattern_words = []
        for replace_word in cls.replace_words:
            if str(sentence).__contains__(replace_word[0]):
                sentence = str(sentence).replace(replace_word[0], replace_word[1])
        set_sentence = set(str(sentence).split(" "))
        for data in cls.recognize_data:
            if received_from in cls.recognize_data[data]["accessible_by"]:
                if len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"]))) > highest_intersection_value:
                    highest_intersection_value = len(set_sentence.intersection(set(cls.recognize_data[data]["pattern_words"])))
                    highest_intersection_tag = data
                    highest_pattern_words = cls.recognize_data[data]["pattern_words"]
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
                triggers = cls.recognize_data[highest_intersection_tag]["trigger"]
                if "integration_home_assistant" in triggers:
                    IntegrationHomeAssistant.check_tag(highest_intersection_tag)
                if "integration_themealdb" in triggers or "integration_thecocktaildb" in triggers:
                    mealName = ' '.join([word for word in str(sentence).split(" ") if word not in highest_pattern_words]).strip()
                    #if word in cls.ignore_stopwords or word not in stopwords.words() and word not in highest_pattern_words
                    mealResponse = IntegrationTheMealDB.search_meal_by_name(mealName)
                    mealStatuscode = mealResponse.status_code
                    if mealStatuscode == 200:
                        meals = mealResponse.json()["meals"]
                        try:
                            if len(meals) > 1:
                                for meal in meals:
                                    if str(meal["strMeal"]).lower() == str(mealName).lower():
                                        meal_data = {"mealName": meal["strMeal"],
                                                     "areaName": meal["strArea"],
                                                     "mealInstructions": meal["strInstructions"],
                                                     "mealIngredients": ", ".join(
                                                         [meal[mealIngredient] for mealIngredient in meal if
                                                          str(mealIngredient).startswith("strIngredient") and meal[
                                                              mealIngredient] != ''])}
                                        answerOption = choice(
                                            cls.recognize_data[highest_intersection_tag]["responses"]["meal"])
                                        return {"forced_behaviour": True,
                                                "answer": answerOption.format(**meal_data),
                                                "tag": highest_intersection_tag}
                            else:
                                meal = meals[0]
                                meal_data = {"mealName": meal["strMeal"],
                                             "areaName": meal["strArea"],
                                             "mealInstructions": meal["strInstructions"],
                                             "mealIngredients": ", ".join(
                                                 [meal[mealIngredient] for mealIngredient in meal if
                                                  str(mealIngredient).startswith("strIngredient") and meal[
                                                      mealIngredient] != ''])}
                                answerOption = choice(
                                    cls.recognize_data[highest_intersection_tag]["responses"]["meal"])
                                return {"forced_behaviour": True,
                                        "answer": answerOption.format(**meal_data),
                                        "tag": highest_intersection_tag}
                        except:
                            cocktailName = ' '.join([word for word in str(sentence).split(" ") if word not in highest_pattern_words]).strip()
                            #if word in cls.ignore_stopwords or word not in stopwords.words() and word not in highest_pattern_words
                            cocktailResponse = IntegrationTheCocktailDB.search_cocktail_by_name(cocktailName)
                            cocktailStatuscode = cocktailResponse.status_code
                            drinks = cocktailResponse.json()["drinks"]
                            try:
                                if cocktailStatuscode == 200:
                                    if len(drinks) > 1:
                                        for drink in drinks:
                                            if str(drink["strDrink"]).lower() == str(cocktailName).lower():
                                                drinkData = {"drinkName": drink["strDrink"],
                                                             "drinkGlass": drink["strGlass"],
                                                             "drinkInstructions": drink["strInstructions"]}
                                                answerOption = choice(
                                                    cls.recognize_data[highest_intersection_tag]["responses"]["cocktail"])
                                                return {"forced_behaviour": True,
                                                        "answer": str(answerOption).format(**drinkData),
                                                        "tag": highest_intersection_tag
                                                        }
                                    else:
                                        drink = drinks[0]
                                        drinkData = {"drinkName": drink["strDrink"], "drinkGlass": drink["strGlass"],
                                                     "drinkInstructions": drink["strInstructions"]}
                                        answerOption = choice(
                                            cls.recognize_data[highest_intersection_tag]["responses"]["cocktail"])
                                        return {"forced_behaviour": True,
                                                "answer": str(answerOption).format(**drinkData),
                                                "tag": highest_intersection_tag
                                                }
                            except:
                                if mealName:
                                    errorData = {"recipe_name": mealName}
                                if cocktailName:
                                    errorData = {"recipe_name": cocktailName}
                                response = str(
                                    choice(cls.recognize_data[highest_intersection_tag]["responses"]["failure_response"])).format(
                                    **errorData)
                                return {"forced_behaviour": True,
                                        "answer": response,
                                        "tag": highest_intersection_tag
                                        }
                if "integration_calendarific" in triggers:
                    holidays = []
                    for holiday in IntegrationCalendarific.get_all_holidays_by_year_and_country_code("DE").json()["response"]["holidays"]:
                        holidayName = holiday["name"]
                        holidayDescription = holiday["description"]
                        holidayDate = holiday["date"]["iso"]
                        holidayType = holiday["type"]
                        holidayStates = ",".join(["All"] if "All" in holiday["states"] else [state["name"] for state in holiday["states"]])
                        holidayData = {"holidayName": holidayName, "holidayDate":holidayDate, "holidayType": ",".join(holidayType)}
                        response = "/n".join(holidays.append(str(choice(cls.recognize_data[highest_intersection_tag]["responses"])).format(**holidayData)))
                    return {"forced_behaviour": True,
                                        "answer": response,
                                        "tag": highest_intersection_tag
                                        }

                if "integration_omdb" in triggers or "integration_tvdb" in triggers:
                    movieName = ' '.join([word for word in str(sentence).split(" ") if word not in highest_pattern_words]).strip()
                    #if word in cls.ignore_stopwords or word not in stopwords.words() and word not in highest_pattern_words
                    movieInformation = IntegrationOMDB.search_by_title(movieName).json()
                    try:
                        movieTitle = movieInformation["Title"]
                        movieYear = movieInformation["Year"]
                        movieGenre = movieInformation["Genre"]
                        moviePlot = movieInformation["Plot"]

                        movieData = {"movieTitle": movieTitle, "movieYear": movieYear, "movieGenre": movieGenre, "moviePlot": moviePlot}
                        response = str(choice(cls.recognize_data[highest_intersection_tag]["responses"]["movie"])).format(**movieData)
                        return {"forced_behaviour": True,
                                "answer": response,
                                "tag": highest_intersection_tag
                                }
                    except:
                        return {"forced_behaviour": True,
                                "answer": str(choice(cls.recognize_data[highest_intersection_tag]["responses"]["failure"])).format(**{"movieTitle": movieName}),
                                "tag": highest_intersection_tag
                                }
                if "integration_audiodb" in triggers:
                    artistName = ' '.join([word for word in str(sentence).split(" ") if word not in highest_pattern_words]).strip()
                    #if word in cls.ignore_stopwords or word not in stopwords.words() and
                    try:
                        artistInformation = \
                        IntegrationTheAudioDB.search_artist_details_by_artist_name(artistName).json()["artists"][0]
                        artistName = artistInformation["strArtist"]
                        artistBiography = artistInformation["strBiographyEN"]

                        artistData = {"artistName": artistName, "artistBiography": artistBiography}
                        response = str(choice(cls.recognize_data[highest_intersection_tag]["responses"]["success"])).format(**artistData)
                        return {"forced_behaviour": True,
                                "answer": response,
                                "tag": highest_intersection_tag
                                }
                    except:
                        return {"forced_behaviour": True,
                                "answer": str(choice(cls.recognize_data[highest_intersection_tag]["responses"]["failure"])).format(**{"artistName": artistName}),
                                "tag": highest_intersection_tag
                                }
            return {"forced_behaviour": True, "answer": choice(cls.recognize_data[highest_intersection_tag]["responses"]), "tag": highest_intersection_tag}
        return {"forced_behaviour": False, "answer": "No result is found", "tag": "error"}

