import datetime
import jwt
import uvicorn
from requests import get
from utilities.dataModels import *
from utilities.settings import Settings
from integrations.integration_ai import IntegrationAi
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from integrations.integration_calendarific import IntegrationCalendarific
from integrations.integration_database import IntegrationDatabase
from integrations.integration_home_assistant import IntegrationHomeAssistant
from integrations.integration_omdb import IntegrationOMDB
from integrations.integration_openlibrary import IntegrationOpenLibrary
#from integrations.integration_openmeteo import IntegrationOpenMeteo
from integrations.integration_pokemon import IntegrationPokemon
from integrations.integration_theaudiodb import IntegrationTheAudioDB
from integrations.integration_thecocktaildb import IntegrationTheCocktailDB
from integrations.integration_themealdb import IntegrationTheMealDB
#from integrations.integration_tvdb import IntegrationTVDB
from integrations.integration_wolframalpha import IntegrationWolframAlpha
#from integrations.integration_home_assistant import IntegrationHomeAssistant

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)

IntegrationAi.load_intents()

def get_country_code():
    ip = get('https://api64.ipify.org?format=json').json()["ip"]
    country_name = get(f'https://ipapi.co/{ip}/json').json()
    return country_name["country"]


def encode_data(data_string):
    return jwt.encode(data_string, algorithm=Settings.get_algorithm(), key=Settings.get_encryption_key())


def decode_data(encoded_data):
    return jwt.decode(encoded_data, algorithms=Settings.get_algorithm(), key=Settings.get_encryption_key())


@app.get("/api/status", tags=["status"])
async def get_api_state():
    return JSONResponse(content={"api_state": True}, status_code=200, media_type="application/json")


@app.post("/api/user/create", tags=["user"])
async def post_user_create(createUser: CreateUser):
    new_username = createUser.username
    new_password = createUser.password
    db_result = IntegrationDatabase.create_new_user(new_username, new_password)
    if db_result == 1:
        return JSONResponse(content={"User creation": True}, status_code=200, media_type="application/json")
    return JSONResponse(content={"User creation": False}, status_code=404, media_type="application/json")


@app.post("/api/user/read", tags=["user"])
async def post_user_read(readUser: ReadUser):
    read_username = readUser.username
    read_password = readUser.password
    db_result = IntegrationDatabase.read_existing_user(read_username, read_password)
    if len(db_result) == 1:
        return JSONResponse(content={"UserId": db_result[0]}, status_code=200, media_type="application/json")
    return JSONResponse(content={"UserId": -1}, status_code=404, media_type="application/json")


@app.patch("/api/user/update", tags=["user"])
async def patch_user_update(updateUser: UpdateUser):
    userID = updateUser.userID
    new_username = updateUser.username
    new_password = updateUser.password
    db_result = IntegrationDatabase.update_existing_user(userID, new_username, new_password)
    if db_result == 1:
        return JSONResponse(content={"User update": True}, status_code=200, media_type="application/json")
    return JSONResponse(content={"User update": False}, status_code=404, media_type="application/json")


@app.delete("/api/user/delete", tags=["user"])
async def put_user_delete(deleteUser: DeleteUser):
    userId = deleteUser.userID
    username = deleteUser.username
    password = deleteUser.password
    db_result = IntegrationDatabase.delete_existing_user(userId, username, password)
    if db_result == 1:
        return JSONResponse(content={"User delete": True}, status_code=200, media_type="application/json")
    return JSONResponse(content={"User delete": False}, status_code=404, media_type="application/json")


@app.post("/api/token/generate", tags=["token"])
async def post_token_generate(tokenData: dict):
    return encode_data(tokenData)


@app.post("/api/ai/check", tags=["ai"])
async def get_command_check(readCommand: ReadCommand):
    OSType = readCommand.OSType
    command = readCommand.command
    return IntegrationAi.check_sentence(command.lower(), OSType)


@app.get("/api/themealdb/search_meal_by_name", tags=["themealdb"])
async def themealdb_get_meal_by_name(mealName: str):
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_name(mealName).json(), status_code=200, media_type="application/json")

@app.get("/api/themealdb/get_random_meal", tags=["themealdb"])
async def themealdb_get_meal_by_name():
    return JSONResponse(content=IntegrationTheMealDB.search_random_meal().json(), status_code=200, media_type="application/json")


@app.get("/api/themealdb/search_meal_by_ingredient", tags=["themealdb"])
async def themealdb_get_meal_by_ingredient(ingredientName: str):
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_ingredient(ingredientName).json(), status_code=200, media_type="application/json")


@app.get("/api/themealdb/search_meal_by_area", tags=["themealdb"])
async def themealdb_get_meal_by_area(areaName: str):
    return JSONResponse(content=IntegrationTheMealDB.search_meal_by_area(areaName).json(), status_code=200, media_type="application/json")

@app.get("/api/thecocktaildb/search_cocktail_by_name", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_name(cocktailName: str):
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktail_by_name(cocktailName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_alcoholic_cocktails", tags=["thecocktaildb"])
async def thecocktaildb_search_alcoholic_cocktails():
    return JSONResponse(content=IntegrationTheCocktailDB.search_alcoholic_cocktails().json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_cocktail_by_glass_name", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_glass_name(glassName: str):
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktails_by_glass(glassName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_cocktail_by_ingredient", tags=["thecocktaildb"])
async def thecocktaildb_search_cocktail_by_ingredient(ingredientName: str):
    return JSONResponse(content=IntegrationTheCocktailDB.search_cocktail_by_ingredient(ingredientName).json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_random_cocktail", tags=["thecocktaildb"])
async def thecocktaildb_search_random_cocktail():
    return JSONResponse(content=IntegrationTheCocktailDB.search_random_cocktail().json(), status_code=200, media_type="application/json")


@app.get("/api/thecocktaildb/search_non_alcoholic_cocktails", tags=["thecocktaildb"])
async def thecocktaildb_search_non_alcoholic_cocktails():
    return JSONResponse(content=IntegrationTheCocktailDB.search_non_alcoholic_cocktails().json(), status_code=200, media_type="application/json")


@app.get("/api/calendarific/get_all_holidays_by_year_and_country_code", tags=["calendarific"])
async def thecocktaildb_search_non_alcoholic_cocktails(country_code = get_country_code(), year = datetime.datetime.now().year):
    return JSONResponse(content=IntegrationCalendarific.get_all_holidays_by_year_and_country_code(country_code).json(), status_code=200, media_type="application/json")


@app.get("/api/omdbapi/search_by_title", tags=["omdbapi"])
async def omdbapi_search_by_title(movieTitle: str):
    return JSONResponse(content=IntegrationOMDB.search_by_title(movieTitle).json(), status_code=200, media_type="application/json")

@app.get("/api/openlibrary/search_by_title", tags=["openlibrary"])
async def openlibrary_search_by_title(bookTitle: str):
    return JSONResponse(content=IntegrationOpenLibrary.search_by_title(bookTitle).json(), status_code=200, media_type="application/json")


@app.get("/api/theaudiodb/search_artist_details_by_artist_name", tags=["theaudiodb"])
async def theaudiodb_search_artist_details_by_artist_name(artistName: str):
    return JSONResponse(content=IntegrationTheAudioDB.search_artist_details_by_artist_name(artistName).json(), status_code=200, media_type="application/json")


@app.post("/api/tables/reset", tags=["tables"])
async def tables_reset():
    IntegrationDatabase.reset_tables()
    return JSONResponse(content={"Reset tables": True}, status_code=200, media_type="application/json")


if __name__ == "__main__":
    IntegrationDatabase.new_database_setup()
    uvicorn.run(app, host=Settings.get_server_ip(), port=Settings.get_server_port())
