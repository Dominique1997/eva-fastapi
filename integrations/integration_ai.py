import json
from integrations.integration_logging import IntegrationLogging as logging
import string
from random import choice
from integrations.integration_omdb import IntegrationOMDB
from integrations.integration_themealdb import IntegrationTheMealDB
from integrations.integration_theaudiodb import IntegrationTheAudioDB
from integrations.integration_calendarific import IntegrationCalendarific
from integrations.integration_wolframalpha import IntegrationWolframAlpha
from integrations.integration_thecocktaildb import IntegrationTheCocktailDB
from integrations.integration_home_assistant import IntegrationHomeAssistant

# TO BE INTEGRATED STILL
# code needs to be fixed
# from integrations.integration_tvdb import IntegrationTVDB
# from integrations.integration_openmeteo import IntegrationOpenMeteo
# from integrations.integration_pokemon import IntegrationPokemon

# recheck needed
# from integrations.integration_openlibrary import IntegrationOpenLibrary


def _handle_calendarific(year, country_code, intent):
    logging.info("Handling integration calendarific")
    holidays = []
    response = ""
    all_holidays = IntegrationCalendarific.get_all_holidays_by_year_and_country_code(country_code, year)
    try:
        if len(all_holidays.json()["response"]["holidays"]) > 1:
            logging.info("Multiple holidays found")
            for holiday in all_holidays.json()["response"]["holidays"]:
                logging.info(f"Found holiday {holiday['name']}")
                holiday_name = holiday["name"]
                holiday_description = holiday["description"]
                holiday_date = holiday["date"]["iso"]
                holiday_type = holiday["type"]
                holiday_states = ",".join(
                    ["All"] if "All" in holiday["states"] else [state["name"] for state in holiday["states"]])
                holiday_data = {"holidayName": holiday_name, "holidayDate": holiday_date, "holidayType": ",".join(holiday_type)}
                holidays.append(str(choice(intent["responses"]["success"])).format(**holiday_data))
            response = "/n".join(holidays)
            logging.info("returning response")
            return {"forced_behaviour": True,
                    "answer": response,
                    }
        elif len(all_holidays.json()["response"]["holidays"]) == 1:
            holiday = all_holidays.json()["response"]["holidays"]
            logging.info(f"Found holiday {holiday['name']}")
            holiday_name = holiday["name"]
            holiday_description = holiday["description"]
            holiday_date = holiday["date"]["iso"]
            holiday_type = holiday["type"]
            holiday_states = ",".join(
                ["All"] if "All" in holiday["states"] else [state["name"] for state in holiday["states"]])
            holiday_data = {"holidayName": holiday_name, "holidayDate": holiday_date, "holidayType": ",".join(holiday_type)}
            holidays.append(str(choice(intent["responses"]["success"])).format(**holiday_data))
            response = "/n".join(holidays)
            logging.info("returning response")
            return {"forced_behaviour": True,
                    "answer": response,
                    }
    except:
        logging.warning(f"Errorcode: 404. Errortext: {all_holidays.text}")
        response = str(choice(intent["responses"]["failure"]))
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_home_assistant(tag, intent):
    logging.info("handling integration home assistant")
    try:
        IntegrationHomeAssistant.post_api_services_by_domain_by_service(intent["domain"], tag)
        logging.info(f"Executing {tag}")
        response = str(choice(intent["responses"]["success"]))
        return {"forced_behaviour": True,
                "answer": response,
                }
    except Exception as e:
        logging.warning(f"An error occured when performing {tag}")
        response = str(choice(intent["responses"]["failure"]))
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_omdb(sentence, intent):
    logging.info("handling integration omdb")
    movie_name = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
    logging.info(f"Found movie name {movie_name}")
    movie_information = IntegrationOMDB.search_by_title(movie_name).json()
    try:
        movie_title = movie_information["Title"]
        movie_year = movie_information["Year"]
        movie_genre = movie_information["Genre"]
        movie_plot = movie_information["Plot"]

        movie_data = {"movieTitle": movie_title, "movieYear": movie_year, "movieGenre": movie_genre, "moviePlot": movie_plot}
        logging.info(f"Found information: {movie_data}")
        response = str(choice(intent["responses"]["movie"])).format(**movie_data)
        return {"forced_behaviour": True,
                "answer": response,
                }
    except:
        logging.warning(f"No information found for {movie_name}")
        response = str(choice(intent["responses"]["failure"])).format(**{"movieTitle": movie_name})
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_theaudiodb(sentence, intent):
    artist_name = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
    artist_information = \
        IntegrationTheAudioDB.search_artist_details_by_artist_name(artist_name).json()
    try:
        artist_name = artist_information["strArtist"]
        artist_biography = artist_information["strBiographyEN"]

        artist_data = {"artistName": artist_name, "artistBiography": artist_biography}
        logging.info(f"Found artist data: {artist_data}")
        response = str(choice(intent["responses"]["success"])).format(**artist_data)
        return {"forced_behaviour": True,
                "answer": response,
                }
    except:
        logging.warning(f"No artist data found for {artist_name}")
        response = str(choice(intent["responses"]["failure"])).format(**{"artistName": artist_name})
        return {"forced_behaviour": True,
                "answer": response,
                }

def _handle_themealdb_or_thecocktaildb(sentence, intent):
    meal_name = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
    meal_response = IntegrationTheMealDB.search_meal_by_name(meal_name)
    meal_statuscode = meal_response.status_code
    if meal_statuscode == 200:
        meals = meal_response.json()["meals"]
        try:
            if len(meals) > 1:
                logging.info(f"Multiple meals found for {meal_name}")
                for meal in meals:
                    if str(meal["strMeal"]).lower() == str(meal_name).lower():
                        meal_data = {"mealName": meal["strMeal"],
                                     "areaName": meal["strArea"],
                                     "mealInstructions": meal["strInstructions"],
                                     "mealIngredients": ", ".join(
                                         [meal[mealIngredient] for mealIngredient in meal if
                                          str(mealIngredient).startswith("strIngredient") and meal[
                                              mealIngredient] != ''])}
                        logging.info(f"Meal found: {meal_data}")

                        answer_option = choice(
                            intent["responses"]["meal"])
                        return {"forced_behaviour": True,
                                "answer": answer_option.format(**meal_data),
                                }
            else:
                meal = meals[0]
                meal_data = {"mealName": meal["strMeal"],
                             "areaName": meal["strArea"],
                             "mealInstructions": meal["strInstructions"],
                             "mealIngredients": ", ".join(
                                 [meal[mealIngredient] for mealIngredient in meal if
                                  str(mealIngredient).startswith("strIngredient") and meal[
                                      mealIngredient] != ''])}
                logging.info(f"Meal found: {meal_data}")
                answer_option = choice(
                    intent["responses"]["meal"])
                return {"forced_behaviour": True,
                        "answer": answer_option.format(**meal_data),
                        }
        except:
            cocktail_name = ' '.join(
                [word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
            cocktail_response = IntegrationTheCocktailDB.search_cocktail_by_name(cocktail_name)
            cocktail_statuscode = cocktail_response.status_code
            drinks = cocktail_response.json()["drinks"]
            try:
                if cocktail_statuscode == 200:
                    if len(drinks) > 1:
                        logging.info(f"Multiple cocktails found for {cocktail_name}")
                        for drink in drinks:
                            if str(drink["strDrink"]).lower() == str(cocktail_name).lower():
                                drink_data = {"drinkName": drink["strDrink"], "drinkGlass": drink["strGlass"], "drinkInstructions": drink["strInstructions"]}
                                logging.info(f"Cocktail found: {drink_data}")
                                answer_option = choice(
                                    intent["responses"]["cocktail"])
                                return {"forced_behaviour": True,
                                        "answer": str(answer_option).format(**drink_data),
                                        }
                    else:
                        drink = drinks[0]
                        drink_data = {"drinkName": drink["strDrink"], "drinkGlass": drink["strGlass"], "drinkInstructions": drink["strInstructions"]}
                        logging.info(f"Cocktail found: {drink_data}")
                        answer_option = choice(
                            intent["responses"]["cocktail"])
                        return {"forced_behaviour": True,
                                "answer": str(answer_option).format(**drink_data),
                                }
            except:
                error_data = {"recipe_name": meal_name or cocktail_name}
                logging.info(f"No meal or cocktail found: {error_data}")
                response = str(choice(intent["responses"]["failure"])).format(**error_data)
                return {"forced_behaviour": True,
                        "answer": response,
                        }


def _execute_intent(intent_name, intent_data, sentence):
    triggers = intent_data["trigger"]
    if "integration_home_assistant" in triggers:
        intent_response = _handle_home_assistant(intent_name, intent_data)
        intent_response["triggers"] = triggers
        return intent_response

    if "integration_themealdb" in triggers or "integration_thecocktaildb" in triggers:
        intent_response = _handle_themealdb_or_thecocktaildb(sentence, intent_data)
        intent_response["triggers"] = triggers
        return intent_response

    if "integration_calendarific" in triggers:
        intent_response = _handle_calendarific("2024", "kdm", intent_data)
        intent_response["triggers"] = triggers
        return intent_response

    if "integration_omdb" in triggers:
        intent_response = _handle_omdb(sentence, intent_data)
        intent_response["triggers"] = triggers
        return intent_response

    if "integration_audiodb" in triggers:
        intent_response = _handle_theaudiodb(sentence, intent_data)
        intent_response["triggers"] = triggers
        return intent_response

    wolframalphaAnswer = IntegrationWolframAlpha.perform_check(sentence)
    wolframalphaAnswer["triggers"] = "wolframalpha"
    logging.info(f"Using wolframalpha as backup: {wolframalphaAnswer}")
    return wolframalphaAnswer

class IntegrationAi:
    intents = json.load(open("json_files/intents.json"))["intents"]
    recognize_data = {}

    def load_intents(self):
        logging.info("Loading intents")
        for intent in self.intents:
            self.recognize_data[intent["tag"]] = {
                "patterns": set(str(''.join(str(char).lower() if char not in string.punctuation else ' ' for char in " ".join(intent["patterns"]))).split(" ")),
                "domain": intent["domain"] if "domain" in intent else [],
                "specific_words": set(" ".join(intent["specific_words"]).split(" ")
                                      if "specific_words" in intent else []),
                "responses": intent["responses"],
                "accessible_by": intent["accessible_by"],
                "trigger": intent["trigger"] if "trigger" in intent else []
            }
            logging.info(f"loaded intent: {intent}")

    def check_sentence(self, sentence, received_from=None):
        logging.info(f"Checking started for {sentence}")
        highest_intersection_value = 0
        highest_intersection_tag = "No result is found"
        highest_intent_data = ""
        set_sentence = set(str(sentence).split(" "))
        for intent_name, intent_data in self.recognize_data.items():
            if received_from in intent_data["accessible_by"]:
                intersection_value = len(intent_data["patterns"].intersection(set_sentence))
                logging.info(f"Intersection of {intersection_value} found between {sentence} and {intent_data['patterns']}")
                specific_words_intersection = len(intent_data["specific_words"].intersection(set_sentence))
                logging.info(f"Intersection of {intersection_value} found between {sentence} and {intent_data['specific_words']}")

                if specific_words_intersection > 0:
                    logging.info(f"Old intersection value: {intersection_value}")
                    intersection_value += specific_words_intersection
                    logging.info(f"Intersection of specific words found and value added: {intersection_value}")

                if intersection_value > 0 and intersection_value > highest_intersection_value:
                    logging.info(f"New highest intersection found: {intent_data}")
                    highest_intersection_value = intersection_value
                    highest_intersection_tag = intent_name
                    highest_intent_data = intent_data

        if highest_intersection_value > 0:
            logging.info(f"Executing highest intent: {highest_intersection_tag}, {highest_intent_data}, {sentence}")
            return _execute_intent(highest_intersection_tag, highest_intent_data, sentence)
        else:
            logging.critical("No intersection found")
            return {"forced_behaviour": False, "answer": "No result is found"}
