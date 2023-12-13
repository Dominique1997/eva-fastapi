import os
import jwt
import uvicorn
from utilities.dataModels import *
from fastapi import FastAPI
from utilities.settings import Settings
from integrations.integration_database import IntegrationDatabase
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from integrations.integration_ai import IntegrationAi as ai
from integrations.integration_logging import IntegrationLogging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
)
ai.load_intents()

def encode_data(data_string):
    return jwt.encode(data_string, algorithm=Settings.get_algorithm(), key=Settings.get_encryption_key())


def decode_data(encoded_data):
    return jwt.decode(encoded_data, algorithms=Settings.get_algorithm(), key=Settings.get_encryption_key())

@app.get("/api/status", tags=["get", "status"])
async def get_api_state():
    IntegrationLogging.log("Checking api state")
    return JSONResponse(content={"api_state": True}, status_code=200, media_type="application/json")

@app.post("/api/user/create", tags=["post", "user"])
async def post_user_create(createUser: CreateUser):
    new_username = createUser.username
    new_password = createUser.password
    db_result = IntegrationDatabase.create_new_user(new_username, new_password)
    if db_result == 1:
        IntegrationLogging.log("Succesfull creation of user")
        return JSONResponse(content={"User creation:": True}, status_code=200, media_type="application/json")
    IntegrationLogging.log("Unsuccesfull creation of user")
    return JSONResponse(content={"User creation:": False}, status_code=404, media_type="application/json")

@app.post("/api/user/read", tags=["post", "user"])
async def post_user_read(readUser: ReadUser):
    read_username = readUser.username
    read_password = readUser.password
    db_result = IntegrationDatabase.read_existing_user(read_username, read_password)
    if len(db_result) == 1:
        IntegrationLogging.log("Succesfull reading of user")
        return JSONResponse(content={"UserId:": db_result[0][0]}, status_code=200, media_type="application/json")
    IntegrationLogging.log("Unsuccesfull reading of user")
    return JSONResponse(content={"UserId:": -1}, status_code=404, media_type="application/json")

@app.post("/api/user/update", tags=["post", "user"])
async def post_user_update(updateUser: UpdateUser):
    userId = updateUser.userId
    new_username = updateUser.username
    new_password = updateUser.password
    db_result = IntegrationDatabase.update_existing_user(userId, new_username, new_password)
    if db_result == 1:
        IntegrationLogging.log("Succesfull updating of user")
        return JSONResponse(content={"User update:": True}, status_code=200, media_type="application/json")
    IntegrationLogging.log("Unsuccesfull updating of user")
    return JSONResponse(content={"User update:": False}, status_code=404, media_type="application/json")

@app.post("/api/user/delete", tags=["post", "user"])
async def post_user_delete(deleteUser: DeleteUser):
    userId = deleteUser.userId
    username = deleteUser.username
    password = deleteUser.password
    db_result = IntegrationDatabase.delete_existing_user(userId, username, password)
    if db_result == 1:
        IntegrationLogging.log("Succesfull deleting of user")
        return JSONResponse(content={"User deletion:": True}, status_code=200, media_type="application/json")
    IntegrationLogging.log("Unsuccesfull deleting of user")
    return JSONResponse(content={"User deletion:": False}, status_code=404, media_type="application/json")

@app.post("/api/tables/reset", tags=["post", "tables"])
async def tables_reset():
    IntegrationDatabase.reset_tables()
    return JSONResponse(content={"Reset tables": True}, status_code=200, media_type="application/json")

if __name__ == "__main__":
    IntegrationDatabase.new_database_setup()
    uvicorn.run(app, host=Settings.get_server_ip(), port=Settings.get_server_port())
