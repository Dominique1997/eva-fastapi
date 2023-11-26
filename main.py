import os
import jwt
import uvicorn
from utilities.dataModels import *
from fastapi import FastAPI
from utilities.settings import Settings
from integrations.integration_database import IntegrationDatabase
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from integrations.integration_wolframalpha import *
from integrations.integration_ai import IntegrationAi as ai
from integrations.integration_logging import IntegrationLogging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
)
ai.load_intents()

def generate_token(data, type_data):
    login_token = jwt.encode(data, key=Settings.get_encryption_key(), algorithm=Settings.get_algorithm())
    IntegrationLogging.log("generated token")
    return JSONResponse(content={type_data: login_token}, media_type="application/json")

def general_check_command(sentence, received_from):
    IntegrationLogging.log("Checking with own ai")
    answer_ai = ai.check_sentence(sentence, received_from)
    if "error" not in answer_ai:
        return JSONResponse(content=answer_ai, media_type="json")
    IntegrationLogging.log("Checking with wolframalpha")
    answer_wolframalpha = IntegrationWolframAlpha.perform_check(sentence)
    if "error" not in answer_wolframalpha:
        IntegrationLogging.log("Wolframalpha has an answer")
        return JSONResponse(content=answer_wolframalpha, media_type="json")
    IntegrationLogging.log("No results were found")
    return JSONResponse(content={"error": "No result is found"}, media_type="application/json")

@app.get("/api/status")
async def get_api_state():
    IntegrationLogging.log("Checking api state")
    return {"api_state": True}

@app.post("/api/login/create_token", tags=["login", "post"])
async def create_login_token(user: User):
    username = user.username
    password = user.password
    data_string = {"username": username, "password": password}
    IntegrationLogging.log("Creating user token")
    return generate_token(data_string, "logged_in_token")

@app.post("/api/login/check_token_validity", tags=["login", "post"])
async def login(login_query: LoginQuery):
    IntegrationLogging.log("Checking validity of token")
    connection_string = jwt.decode(login_query.login_query, key=Settings.get_encryption_key(), algorithms=[Settings.get_algorithm()])
    username = connection_string["username"]
    password = connection_string["password"]
    if Settings.test_mode():
        IntegrationLogging.log("Checking on local database")
        db_response = IntegrationDatabase.select_local_user(username, password)
    else:
        IntegrationLogging.log("Checking on external database")
        db_response = IntegrationDatabase.select_extern_user(username, password)
    if db_response["Login_state"] == "logged_in":
        IntegrationLogging.log("Valid user is found")
        login_time = datetime.now().strftime('%m/%d/%y %H:%M:%S')
        connection_string["login_time"] = str(login_time)
        connection_string["logout_time"] = str(datetime.strptime(login_time, '%m/%d/%y %H:%M:%S') + Settings.get_delta_time())
    return generate_token(connection_string, "validated_token")

@app.post("/api/{program_type}/check_command", tags=["windows", "discord", "post"])
async def check_command(check_command: CheckQuery):
    IntegrationLogging.log("Checking received sentence")
    return general_check_command(check_command.sentence, check_command.program_type)

@app.post("/api/user/create", tags=["user", "post"])
async def create_new_user(new_user: NewUser):
    if Settings.test_mode():
        IntegrationLogging.log("Creating local user")
        db_response = IntegrationDatabase.create_local_new_user(new_user.username, new_user.password)
    else:
        IntegrationLogging.log("Creating external user")
        db_response = IntegrationDatabase.create_extern_new_user(new_user.username, new_user.password)
    return JSONResponse(content=db_response, media_type="json")

@app.put("/api/user/update/general", tags=["user", "put"])
async def update_existing_user(update_user_general: UpdateUserGeneral):
    if Settings.test_mode():
        IntegrationLogging.log("Updating local user")
        db_response = IntegrationDatabase.update_local_user(update_user_general.userid, update_user_general.new_username, update_user_general.new_password)
    else:
        IntegrationLogging.log("Updating external user")
        db_response = IntegrationDatabase.update_extern_user(update_user_general.userid, update_user_general.new_username, update_user_general.new_password)
    return JSONResponse(content=db_response, media_type="json")

@app.delete("/api/user/delete", tags=["user", "delete"])
async def delete_existing_user(delete_user: DeleteUser):
    if Settings.test_mode():
        IntegrationLogging.log("Deleting local user")
        db_response = IntegrationDatabase.delete_local_user(delete_user.userid)
    else:
        IntegrationLogging.log("deleting external user")
        db_response = IntegrationDatabase.delete_extern_user(delete_user.userid)
    return JSONResponse(content=db_response, media_type="json")

@app.post("/api/user/select", tags=["user", "post"])
async def select_existing_user(select_user: SelectUser):
    if Settings.test_mode():
        IntegrationLogging.log("Selecting local user")
        db_response = IntegrationDatabase.select_local_user(select_user.username, select_user.password)
    else:
        IntegrationLogging.log("Selecting external user")
        db_response = IntegrationDatabase.select_extern_user(select_user.username, select_user.password)
    return JSONResponse(content=db_response, media_type="json")

@app.post("/api/token/add", tags=["token", "post"])
async def add_user_token(add_token: AddToken):
    if Settings.test_mode():
        IntegrationLogging.log("Creating local token")
        IntegrationDatabase.add_local_user_token(add_token.userID, add_token.server_ip, add_token.server_port, add_token.server_username, add_token.server_password, add_token.server_token)
    else:
        IntegrationLogging.log("Creating external token")
        IntegrationDatabase.add_extern_user_token(add_token.userID, add_token.server_ip, add_token.server_port,
                                                          add_token.server_username, add_token.server_password,
                                                          add_token.server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")


@app.put("/api/token/update/general", tags=["token", "put"])
async def update_user_token(update_token: UpdateTokenGeneral):
    if Settings.test_mode():
        IntegrationLogging.log("Updating local token")
        IntegrationDatabase.update_local_user_token(update_token.tokenID, update_token.userID, update_token.server_ip, update_token.server_port, update_token.server_username, update_token.server_password, update_token.server_token)
    else:
        IntegrationLogging.log("Updating external token")
        IntegrationDatabase.update_extern_user_token(update_token.tokenID, update_token.userID, update_token.server_ip, update_token.server_port, update_token.server_username, update_token.server_password, update_token.server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")


@app.patch("/api/token/update/server_ip", tags=["token", "patch"])
async def update_user_token_server_ip(update_users_token_ip: UpdateTokenServerIP):
    if Settings.test_mode():
        IntegrationLogging.log("Updating local server ip")
        IntegrationDatabase.update_local_user_token(update_users_token_ip.tokenID, update_users_token_ip.userID, update_users_token_ip.server_ip)
    else:
        IntegrationLogging.log("Updating external server ip")
        IntegrationDatabase.update_extern_user_token(update_users_token_ip.tokenID, update_users_token_ip.userID, update_users_token_ip.server_ip)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_port", tags=["token", "patch"])
async def update_user_token(update_users_token_port: UpdateTokenServerPort):
    if Settings.test_mode():
        IntegrationLogging.log("Update local server port")
        IntegrationDatabase.update_local_user_token(update_users_token_port.tokenID, update_users_token_port.userID, update_users_token_port.server_port)
    else:
        IntegrationLogging.log("Update external server port")
        IntegrationDatabase.update_extern_user_token(update_users_token_port.tokenID, update_users_token_port.userID, update_users_token_port.server_port)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.put("/api/token/update/server_username", tags=["token", "patch"])
async def update_user_token(update_server_username: UpdateServerUsername):
    if Settings.test_mode():
        IntegrationLogging.log("Update local server username")
        IntegrationDatabase.update_local_user_token(update_server_username.tokenID, update_server_username.userID, update_server_username.server_username)
    else:
        IntegrationLogging.log("Update external server username")
        IntegrationDatabase.update_extern_user_token(update_server_username.tokenID, update_server_username.userID, update_server_username.server_username)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")


@app.put("/api/token/update/server_password", tags=["token", "patch"])
async def update_user_token(update_server_user_password: UpdateUserPassword):
    if Settings.test_mode():
        IntegrationLogging.log("Update local server password")
        IntegrationDatabase.update_local_user_token(update_server_user_password.tokenID, update_server_user_password.userID, update_server_user_password.server_password)
    else:
        IntegrationLogging.log("Update external server password")
        IntegrationDatabase.update_extern_user_token(update_server_user_password.tokenID, update_server_user_password.userID, update_server_user_password.server_password)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")


@app.put("/api/token/update/server_token", tags=["token", "patch"])
async def update_user_token(update_server_token: UpdateServerToken):
    if Settings.test_mode():
        IntegrationLogging.log("Update local server token")
        IntegrationDatabase.update_local_user_token(update_server_token.tokenID, update_server_token.userID, update_server_token.server_token)
    else:
        IntegrationLogging.log("Update external server token")
        IntegrationDatabase.update_extern_user_token(update_server_token.tokenID, update_server_token.userID, update_server_token.server_token)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.post("/api/token/select", tags=["token", "post"])
async def select_user_token(select_server_token: SelectServerToken):
    if Settings.test_mode():
        IntegrationLogging.log("Select local token")
        IntegrationDatabase.select_local_user_token(select_server_token.tokenid, select_server_token.userid)
    else:
        IntegrationLogging.log("Select external token")
        IntegrationDatabase.select_extern_user_token(select_server_token.tokenid, select_server_token.userid)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

@app.post("/api/token/delete", tags=["token", "post"])
async def delete_user_token(delete_server_token: DeleteServerToken):
    if Settings.test_mode():
        IntegrationLogging.log("Delete local token")
        IntegrationDatabase.delete_local_user_token(delete_server_token.tokenid, delete_server_token.userid)
    else:
        IntegrationLogging.log("Delete external token")
        IntegrationDatabase.delete_extern_user_token(delete_server_token.tokenid, delete_server_token.userid)
    return JSONResponse(content={"Result": "DONE"}, media_type="json")

if __name__ == "__main__":
    if Settings.test_mode():
        if not os.path.exists("eva-database.db"):
            IntegrationDatabase.new_local_database_setup()
    uvicorn.run(app, host=Settings.get_server_ip(), port=Settings.get_server_port())
