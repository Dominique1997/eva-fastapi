import os
import jwt
import uvicorn
from dataModels import *
from fastapi import FastAPI
from settings import Settings
from database import Database
from datetime import datetime
from fastapi.responses import JSONResponse
from integrations.integration_wolframalpha import *
from integrations.integration_ai import IntegrationAi as ai

app = FastAPI()
ai.load_intents()

def generate_token(data, type_data):
    login_token = jwt.encode(data, key=Settings.get_encryption_key(), algorithm=Settings.get_algorithm())
    return JSONResponse(content={type_data: login_token}, media_type="application/json")

def general_check_command(sentence, received_from):
    answer_ai = ai.check_sentence(sentence, received_from)
    if "error" not in answer_ai:
        print("ai")
        return JSONResponse(content=answer_ai, media_type="json")
    answer_wolframalpha = IntegrationWolframAlpha.perform_check(sentence)
    if "error" not in answer_wolframalpha:
        print("wolframalpha")
        return JSONResponse(content=answer_wolframalpha, media_type="json")
    print("error")
    return JSONResponse(content={"error": "No result is found"}, media_type="application/json")

@app.get("/api/status")
async def get_api_state():
    return {"api_state": True}

@app.post("/api/login/create_token", tags=["login", "post"])
async def create_login_token(user: User):
    username = user.username
    password = user.password
    data_string = {"username": username, "password": password}

    return generate_token(data_string, "logged_in_token")

@app.post("/api/login/check_token_validity", tags=["login", "post"])
async def login(login_query: Login_query):
    connection_string = jwt.decode(login_query.login_query, key=Settings.get_encryption_key(), algorithms=[Settings.get_algorithm()])
    username = connection_string["username"]
    password = connection_string["password"]
    db_response = Database.select_user(username, password)
    if db_response["Login_state"] == "logged_in":
        login_time = datetime.now().strftime('%m/%d/%y %H:%M:%S')
        connection_string["login_time"] = str(login_time)
        connection_string["logout_time"] = str(datetime.strptime(login_time, '%m/%d/%y %H:%M:%S') + Settings.get_delta_time())
    return generate_token(connection_string, "validated_token")

@app.get("/api/{program_type}/check_command", tags=["windows", "discord", "get"])
async def check_command(sentence, program_type):
    return general_check_command(sentence, program_type)

@app.post("/api/user/create", tags=["user", "post"])
async def create_new_user(username, password):
    db_response = Database.create_new_user(username, password)
    return JSONResponse(content=db_response, media_type="json")

@app.put("/api/user/update/general", tags=["user", "put"])
async def update_existing_user(userid, new_username, new_password):
    db_response = Database.update_user(userid, new_username, new_password)
    return JSONResponse(content=db_response, media_type="json")

@app.patch("/api/user/update/username", tags=["user", "patch"])
async def update_existing_user(userid, new_username):
    db_response = Database.update_user(userid, new_username)
    return JSONResponse(content=db_response, media_type="json")

@app.put("/api/user/update/password", tags=["user", "patch"])
async def update_existing_user(userid, new_password):
    db_response = Database.update_user(userid, new_password)
    return JSONResponse(content=db_response, media_type="json")

@app.delete("/api/user/delete", tags=["user", "delete"])
async def delete_existing_user(userid):
    db_response = Database.delete_user(userid)
    return JSONResponse(content=db_response, media_type="json")

@app.post("/api/user/select", tags=["user", "post"])
async def select_existing_user(program_type, username, password, discord_name="undefined"):
    db_response = Database.select_user(program_type, username, password, discord_name)
    return JSONResponse(content=db_response, media_type="json")

@app.post("/api/token/add", tags=["token", "post"])
async def add_user_token(userID, server_ip, server_port, server_username, server_password, server_token):
    Database.add_user_token(userID, server_ip, server_port, server_username, server_password, server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/general", tags=["token", "put"])
async def update_user_token(tokenID, userID, server_ip, server_port, server_username, server_password, server_token):
    Database.update_user_token(tokenID, userID, server_ip, server_port, server_username, server_password, server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.patch("/api/token/update/server_ip", tags=["token", "patch"])
async def update_user_token(tokenID, userID, server_ip):
    Database.update_user_token(tokenID, userID, server_ip)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_port", tags=["token", "patch"])
async def update_user_token(tokenID, userID, server_port):
    Database.update_user_token(tokenID, userID, server_port)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_username", tags=["token", "patch"])
async def update_user_token(tokenID, userID, server_username):
    Database.update_user_token(tokenID, userID, server_username)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_password", tags=["token", "patch"])
async def update_user_token(tokenID, userID, server_password):
    Database.update_user_token(tokenID, userID, server_password)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_token", tags=["token", "patch"])
async def update_user_token(tokenID, userID, server_token):
    Database.update_user_token(tokenID, userID, server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.post("/api/token/select", tags=["token", "post"])
async def select_user_token(tokenid, userid):
    Database.select_user_token(tokenid, userid)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.post("/api/token/delete", tags=["token", "post"])
async def delete_user_token(tokenid, userid):
    Database.delete_user_token(tokenid, userid)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

if __name__ == "__main__":
    if not os.path.exists("eva-database.db"):
        Database.new_database_setup()
    uvicorn.run(app, host="0.0.0.0", port=80)
