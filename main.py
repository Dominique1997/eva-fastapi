import datetime
import uvicorn
import jwt
import string
from integrations.integration_logging import IntegrationLogging as logging
from utilities.dataModels import *
from utilities.settings import Settings
from integrations.integration_ai import IntegrationAi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from integrations.integration_calendarific import IntegrationCalendarific
from integrations.integration_database import IntegrationDatabase
from integrations.integration_openmeteo import IntegrationOpenMeto
from integrations.integration_omdb import IntegrationOMDB
from integrations.tobechecked_integration_openlibrary import IntegrationOpenLibrary
#from integrations.integration_openmeteo import IntegrationOpenMeteo
from integrations.integration_theaudiodb import IntegrationTheAudioDB
from integrations.integration_thecocktaildb import IntegrationTheCocktailDB
from integrations.integration_themealdb import IntegrationTheMealDB
#from integrations.integration_tvdb import IntegrationTVDB
from integrations.integration_wolframalpha import IntegrationWolframAlpha
import languagemodels
#from integrations.integration_home_assistant import IntegrationHomeAssistant

integrationAI = IntegrationAi()
integrationAI.load_intents()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)


def get_country_code():
    #ip = get('https://api64.ipify.org?format=json').json()["ip"]
    #country_name = get(f'https://ipapi.co/{ip}/json').json()
    #print(country_name)
    return "Belgium"
    #country_name["country"]


def encode_data(data_string):
    logging.info(f"encoding {data_string}")
    return jwt.encode(data_string, algorithm=Settings.get_algorithm(), key=Settings.get_encryption_key())


def decode_data(encoded_data):
    logging.info(f"decoding {encoded_data}")
    return jwt.decode(encoded_data, algorithms=Settings.get_algorithm(), key=Settings.get_encryption_key())


@app.get("/api/status", tags=["status"])
async def get_api_state():
    logging.info("returning api state")
    return JSONResponse(content={"api_state": True}, status_code=200, media_type="application/json")


@app.post("/api/ai/check", tags=["ai"])
async def get_command_check(readCommand: ReadCommand):
    OSType = readCommand.OSType
    command = str(readCommand.command).lower()
    for punctuation in string.punctuation:
        command = str(command).replace(punctuation, "")
    logging.info(f"Checking the sentence {command} received from {OSType}")
    return integrationAI.check_sentence(command.lower(), OSType)


@app.get("/api/themealdb/search_meal_by_name", tags=["themealdb"])
async def themealdb_get_meal_by_name(mealName: str):
    logging.info(f"Checking information for a meal by the name {mealName}")
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_name(mealName).json(), status_code=200, media_type="application/json")


@app.get("/api/themealdb/get_random_meal", tags=["themealdb"])
async def themealdb_get_meal_by_name():
    logging.info(f"Checking information for a random meal")
    return JSONResponse(content=IntegrationTheMealDB.search_random_meal().json(), status_code=200, media_type="application/json")


@app.get("/api/themealdb/search_meal_by_ingredient", tags=["themealdb"])
async def themealdb_get_meal_by_ingredient(ingredientName: str):
    logging.info(f"Checking information for a meal by the ingredient {ingredientName}")
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_ingredient(ingredientName).json(), status_code=200, media_type="application/json")


@app.get("/api/themealdb/search_meal_by_area", tags=["themealdb"])
async def themealdb_get_meal_by_area(areaName: str):
    logging.info(f"Checking information for a meal by the area {areaName}")
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_area(areaName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_cocktail_by_name", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_name(cocktailName: str):
    logging.info(f"Checking information for a cocktail by the name {cocktailName}")
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktail_by_name(cocktailName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_alcoholic_cocktails", tags=["thecocktaildb"])
async def thecocktaildb_search_alcoholic_cocktails():
    logging.info(f"Checking information for alocholic cocktails")
    return JSONResponse(content=IntegrationTheCocktailDB.search_alcoholic_cocktails().json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_cocktail_by_glass_name", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_glass_name(glassName: str):
    logging.info(f"Checking information for a cocktail by the type of glass {glassName}")
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktails_by_glass(glassName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_cocktail_by_ingredient", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_ingredient(ingredientName: str):
    logging.info(f"Checking information for a cocktail by the ingredient {ingredientName}")
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktail_by_ingredient(ingredientName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_random_cocktail", tags=["thecocktaildb"])
async def thecocktaildb_search_random_cocktail():
    logging.info(f"Checking information for a random cocktail")
    return JSONResponse(content=IntegrationTheCocktailDB.search_random_cocktail().json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_non_alcoholic_cocktails", tags=["thecocktaildb"])
async def thecocktaildb_search_non_alcoholic_cocktails():
    logging.info(f"Checking information for a non alcoholic cocktail")
    return JSONResponse(content=IntegrationTheCocktailDB.search_non_alcoholic_cocktails().json(), status_code=200, media_type="application/json")


@app.get("/api/calendarific/get_all_holidays_by_year_and_country_code", tags=["calendarific"])
async def calendarific_get_all_holidays_by_year_and_country_code(country_code = get_country_code(), year = datetime.datetime.now().year):
    logging.info(f"Checking information for all holidays for {country_code} in the year {year}")
    return JSONResponse(content=IntegrationCalendarific.get_all_holidays_by_year_and_country_code(country_code).json(), status_code=200, media_type="application/json")


@app.get("/api/omdbapi/search_by_title", tags=["omdbapi"])
async def omdbapi_search_by_title(movieTitle: str):
    logging.info(f"Checking information for the movie {movieTitle}")
    return JSONResponse(content=IntegrationOMDB.search_by_title(movieTitle).json(), status_code=200, media_type="application/json")


@app.get("/api/openlibrary/search_by_title", tags=["openlibrary"])
async def openlibrary_search_by_title(bookTitle: str):
    logging.info(f"Checking information for the book {bookTitle}")
    return JSONResponse(content=IntegrationOpenLibrary.search_by_title(bookTitle).json(), status_code=200, media_type="application/json")


@app.get("/api/theaudiodb/search_artist_details_by_artist_name", tags=["theaudiodb"])
async def theaudiodb_search_artist_details_by_artist_name(artistName: str):
    logging.info(f"Checking information for the artist {artistName}")
    return JSONResponse(content=IntegrationTheAudioDB.search_artist_details_by_artist_name(artistName).json(), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_rain_percentage_today", tags=["openmeteo"])
async def openmeteo_get_rain_percentage_today():
    logging.info(f"Checking weather rain data today")
    return JSONResponse(content=IntegrationOpenMeto.get_rain_percentage(), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_rain_percentage_tomorrow", tags=["openmeteo"])
async def openmeteo_get_rain_percentage_tomorrow():
    logging.info(f"Checking weather rain data tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_rain_percentage(1), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_rain_percentage_the_day_after_tomorrow", tags=["openmeteo"])
async def openmeteo_get_rain_percentage_the_day_after_tomorrow():
    logging.info(f"Checking weather rain data the day after tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_rain_percentage(2), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_snowfall_hourly_today", tags=["openmeteo"])
async def openmeteo_get_snowfall_today():
    logging.info(f"Checking snowfall rain data today")
    return JSONResponse(content=IntegrationOpenMeto.get_snowfall_percentage(), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_snowfall_hourly_tomorrow", tags=["openmeteo"])
async def openmeteo_get_snowfall_hourly_tomorrow():
    logging.info(f"Checking snowfall rain data tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_snowfall_percentage(1), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_snowfall_hourly_the_day_after_tomorrow", tags=["openmeteo"])
async def openmeteo_get_snowfall_hourly_the_day_after_tomorrow():
    logging.info(f"Checking snowfall rain data the_day_after_tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_snowfall_percentage(2), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_cloud_cover_hourly_today", tags=["openmeteo"])
async def openmeteo_get_cloud_cover_hourly_today():
    logging.info(f"Checking cloud cover data today")
    return JSONResponse(content=IntegrationOpenMeto.get_cloud_cover_percentage(), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_cloud_cover_hourly_tomorrow", tags=["openmeteo"])
async def openmeteo_get_cloud_cover_hourly_tomorrow():
    logging.info(f"Checking cloud cover data tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_cloud_cover_percentage(1), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_cloud_cover_hourly_the_day_after_tomorrow", tags=["openmeteo"])
async def openmeteo_get_cloud_cover_hourly_the_day_after_tomorrow():
    logging.info(f"Checking cloud cover data tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_cloud_cover_percentage(2), status_code=200, media_type="application/json")


@app.get("/api/openmeteo/get_cloud_cover_hourly_the_day_after_tomorrow", tags=["openmeteo"])
async def openmeteo_get_cloud_cover_hourly_the_day_after_tomorrow():
    logging.info(f"Checking cloud cover data the day after tomorrow")
    return JSONResponse(content=IntegrationOpenMeto.get_cloud_cover_percentage(), status_code=200, media_type="application/json")


@app.get("/api/languagemodel", tags=["languagemodel"])
async def languagemodel_get_response(input: str):
    logging.info(f"Checking languagemodel")
    return JSONResponse(content=languagemodels.do(input), status_code=200, media_type="application/json")


@app.post("/api/tables/reset", tags=["tables"])
async def tables_reset():
    logging.info(f"Resetting the tables")
    IntegrationDatabase.reset_tables()
    return JSONResponse(content={"Reset tables": True}, status_code=200, media_type="application/json")


if __name__ == "__main__":
    IntegrationDatabase.new_database_setup()
    uvicorn.run(app, host=Settings.get_server_ip(), port=Settings.get_server_port())
