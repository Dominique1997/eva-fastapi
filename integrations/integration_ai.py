import json
import logging
from random import choice
from integrations.integration_omdb import IntegrationOMDB
from integrations.integration_themealdb import IntegrationTheMealDB
from integrations.integration_theaudiodb import IntegrationTheAudioDB
from integrations.integration_calendarific import IntegrationCalendarific
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
    try:
        all_holidays = \
        IntegrationCalendarific.get_all_holidays_by_year_and_country_code(country_code, year).json()["response"][
            "holidays"]
        for holiday in all_holidays:
            logging.info(f"Found holiday {holiday['name']}")
            holidayName = holiday["name"]
            holidayDescription = holiday["description"]
            holidayDate = holiday["date"]["iso"]
            holidayType = holiday["type"]
            holidayStates = ",".join(
                ["All"] if "All" in holiday["states"] else [state["name"] for state in holiday["states"]])
            holidayData = {"holidayName": holidayName, "holidayDate": holidayDate, "holidayType": ",".join(holidayType)}
            holidays.append(str(choice(intent["responses"]["success"])).format(**holidayData))
        response = "/n".join(holidays)
        logging.info("returning response")
        return {"forced_behaviour": True,
                "answer": response,
                }
    except:
        response = str(choice(intent["responses"]["failure"]))
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_home_assistant(tag, intent):
    logging.info("handling integration home assistant")
    try:
        IntegrationHomeAssistant.post_api_services_by_domain_by_service(intent["domain"], tag)
        response = str(choice(intent["responses"]["success"]))
        return {"forced_behaviour": True,
                "answer": response,
                }
    except Exception as e:
        response = str(choice(intent["responses"]["failure"]))
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_omdb(sentence, intent):
    logging.info("handling integration omdb")
    movieName = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
    logging.info(f"Found movie name {movieName}")
    movieInformation = IntegrationOMDB.search_by_title(movieName).json()
    try:
        movieTitle = movieInformation["Title"]
        movieYear = movieInformation["Year"]
        movieGenre = movieInformation["Genre"]
        moviePlot = movieInformation["Plot"]

        movieData = {"movieTitle": movieTitle, "movieYear": movieYear, "movieGenre": movieGenre,
                     "moviePlot": moviePlot}
        response = str(choice(intent["responses"]["movie"])).format(**movieData)
        return {"forced_behaviour": True,
                "answer": response,
                }
    except:
        response = str(choice(intent["responses"]["failure"])).format(**{"movieTitle": movieName})
        return {"forced_behaviour": True,
                "answer": response,
                }


def _handle_theaudiodb(sentence, intent):
    artistName = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
    try:
        artistInformation = \
            IntegrationTheAudioDB.search_artist_details_by_artist_name(artistName).json()
        artistName = artistInformation["strArtist"]
        artistBiography = artistInformation["strBiographyEN"]

        artistData = {"artistName": artistName, "artistBiography": artistBiography}
        response = str(choice(intent["responses"]["success"])).format(**artistData)
        return {"forced_behaviour": True,
                "answer": response,
                }
    except:
        response = str(choice(intent["responses"]["failure"])).format(**{"artistName": artistName})
        return {"forced_behaviour": True,
                "answer": response,
                }

def _handle_themealdb_or_thecocktaildb(sentence, intent):
    mealName = ' '.join([word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
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
                            intent["responses"]["meal"])
                        return {"forced_behaviour": True,
                                "answer": answerOption.format(**meal_data),
                                "type": "meal"
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
                answerOption = choice(
                    intent["responses"]["meal"])
                return {"forced_behaviour": True,
                        "answer": answerOption.format(**meal_data),
                        "type": "meal"
                        }
        except:
            cocktailName = ' '.join(
                [word for word in str(sentence).split(" ") if word not in intent["patterns"]]).strip()
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
                                    intent["responses"]["cocktail"])
                                return {"forced_behaviour": True,
                                        "answer": str(answerOption).format(**drinkData),
                                        "type": "drink"
                                        }
                    else:
                        drink = drinks[0]
                        drinkData = {"drinkName": drink["strDrink"], "drinkGlass": drink["strGlass"],
                                     "drinkInstructions": drink["strInstructions"]}
                        answerOption = choice(
                            intent["responses"]["cocktail"])
                        return {"forced_behaviour": True,
                                "answer": str(answerOption).format(**drinkData),
                                "type": "drink"
                                }
            except:
                if mealName:
                    errorData = {"recipe_name": mealName}
                if cocktailName:
                    errorData = {"recipe_name": cocktailName}
                response = str(choice(intent["responses"]["failure"])).format(**errorData)
                return {"forced_behaviour": True,
                        "answer": response,
                        }


def _execute_intent(intent_name, intent_data, sentence):
    triggers = intent_data["trigger"]
    if "integration_home_assistant" in triggers:
        return _handle_home_assistant(intent_name, intent_data)

    if "integration_themealdb" in triggers or "integration_thecocktaildb" in triggers:
        return _handle_themealdb_or_thecocktaildb(sentence, intent_data)

    if "integration_calendarific" in triggers:
        return _handle_calendarific("2024", "kdm", intent_data)

    if "integration_omdb" in triggers:
        return _handle_omdb(sentence, intent_data)

    if "integration_audiodb" in triggers:
        return _handle_theaudiodb(sentence, intent_data)

    return {"forced_behaviour": True, "answer": "eva did not recognize your input"}


class IntegrationAi:
    intents = json.load(open("json_files/intents.json"))["intents"]
    recognize_data = {}

    def load_intents(self):
        for intent in self.intents:
            self.recognize_data[intent["tag"]] = {
                "patterns": set(" ".join(intent["patterns"]).split(" ")),
                "domain": intent["domain"] if "domain" in intent else [],
                "specific_words": set(" ".join(intent["specific_words"]).split(" ") if "specific_words" in intent else []),
                "responses": intent["responses"],
                "accessible_by": intent["accessible_by"],
                "trigger": intent["trigger"] if "trigger" in intent else []
            }

    def check_sentence(self, sentence, received_from=None):
        highest_intersection_value = 0
        highest_intersection_tag = "No result is found"
        highest_intent_data = ""
        set_sentence = set(str(sentence).split(" "))
        for intent_name, intent_data in self.recognize_data.items():
            if received_from in intent_data["accessible_by"]:
                intersection_value = len(intent_data["patterns"].intersection(set_sentence))
                specific_words_intersection = len(intent_data["specific_words"].intersection(set_sentence))

                # Check if specific words are present in the sentence
                if specific_words_intersection > 0:
                    intersection_value += specific_words_intersection

                if intersection_value > 0 and intersection_value > highest_intersection_value:
                    highest_intersection_value = intersection_value
                    highest_intersection_tag = intent_name
                    highest_intent_data = intent_data

        if highest_intersection_value > 0:
            return _execute_intent(highest_intersection_tag, highest_intent_data, sentence)
        else:
            return {"forced_behaviour": False, "answer": "No result is found", "tag": "error"}
