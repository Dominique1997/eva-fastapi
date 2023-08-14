import os
import jwt
import uvicorn
from ai import ai
from fastapi import *
from settings import Settings
from database import Database
from datetime import datetime
from integrations.integration_wolframalpha import *


app = FastAPI()
#settings = json.load(open("settings.json"))
ai.load_intents()

@app.get("/api/status")
async def get_api_state():
    return {"api_state": True}

@app.get("/api/general/check_command")
async def general_check_command(sentence):
    answer_wolframalpha = IntegrationWolframAlpha.perform_check(sentence)
    answer_ai = ai.check_sentence(sentence)
    if "error" not in answer_wolframalpha:
        return json.loads(answer_wolframalpha)
    if "error" not in answer_ai:
        return json.loads(answer_ai)
    return {"error": "No result is found"}

@app.get("/api/login")
async def login(username, password):
    connection_string = jwt.encode({"username": username, "password": password}, key=Settings.get_encryption_key(), algorithm=Settings.get_algorithm())
    db_response = Database.select_user(connection_string)
    if db_response["Login_state"] == "logged_in":
        login_time = datetime.now()
        db_response["login_time"] = login_time
        db_response["logout_time"] = login_time + Settings.get_delta_time()
    return db_response

@app.post("/api/create_new_user")
async def create_new_user(username, password):
    pass


if __name__ == "__main__":
    if not os.path.exists("eva-database.db"):
        Database.new_database_setup()
    uvicorn.run(app, host="0.0.0.0", port=5001)


