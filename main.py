import os
import jwt
import uvicorn
from fastapi import *
from settings import Settings
from database import Database
from datetime import datetime
from fastapi.responses import JSONResponse
from integrations.integration_wolframalpha import *


app = FastAPI()
ai.load_intents()


@app.get("/api/status")
async def get_api_state():
    return {"api_state": True}

@app.get("/create/login/token")
async def create_login_token(username="", password="", discord_username="", program_type=""):
    login_token = jwt.encode({"username": username, "password": password, "discord_username": discord_username, "program_type": program_type}, key=Settings.get_encryption_key(), algorithm=Settings.get_algorithm())
    return JSONResponse(content={"login_token": login_token}, media_type="application/json")


@app.get("/api/general/check_command")
async def general_check_command(sentence):
    answer_ai = ai.check_sentence(sentence)
    answer_wolframalpha = IntegrationWolframAlpha.perform_check(sentence)
    if "error" not in answer_ai:
        return JSONResponse(content=answer_ai, media_type="json")
    if "error" not in answer_wolframalpha:
        return JSONResponse(content=answer_wolframalpha, media_type="json")
    return JSONResponse(content={"error": "No result is found"}, media_type="application/json")


@app.get("/api/login/{login_query}")
async def login(login_query):
    print(login_query)
    connection_string = jwt.decode(login_query, key=Settings.get_encryption_key(), algorithms=[Settings.get_algorithm()])
    username = connection_string["username"]
    discord_username = connection_string["discord_username"]
    password = connection_string["password"]
    program_type = connection_string["program_type"]
    db_response = Database.select_user(program_type, username, password, discord_username)
    if db_response["Login_state"] == "logged_in":
        login_time = datetime.now()
        db_response["login_time"] = login_time
        db_response["logout_time"] = login_time + Settings.get_delta_time()
    return JSONResponse(content=db_response, media_type="application/json")


@app.post("/api/create_new_user")
async def create_new_user(username, password):
    db_response = Database.create_new_user(username, password)
    return JSONResponse(content=db_response, media_type="application/json")


@app.post("/api/update_existing_user")
async def update_existing_user(userid, new_username, new_password):
    db_response = Database.update_user(userid, new_username, new_password)
    return JSONResponse(content=db_response, media_type="application/json")


@app.post("/api/delete_existing_user")
async def delete_existing_user(userid):
    db_response = Database.delete_user(userid)
    return JSONResponse(content=db_response, media_type="application/json")


@app.post("/api/select_existing_user")
async def select_existing_user(username, password):
    db_response = Database.select_user(username, password)
    return JSONResponse(content=db_response, media_type="application/json")

@app.post("/api/add_user_token")
async def add_user_token(userID, server_ip, server_port, server_username, server_password, server_token):
    Database.add_user_token(userID, server_ip, server_port, server_username, server_password, server_token)
    return {"Result": "DONE"}

@app.post("/api/update_user_token")
async def add_user_token(tokenID, userID, server_ip, server_port, server_username, server_password, server_token):
    Database.update_user_token(tokenID, userID, server_ip, server_port, server_username, server_password, server_token)
    return {"Result": "DONE"}

@app.post("/api/select_user_token")
async def select_user_token(tokenid, userid):
    Database.select_user_token(tokenid, userid)

@app.post("/api/delete_user_token")
async def delete_user_token(tokenid, userid):
    Database.delete_user_token(tokenid, userid)


if __name__ == "__main__":
    if not os.path.exists("eva-database.db"):
        Database.new_database_setup()
    uvicorn.run(app, host="0.0.0.0", port=5001)


