import os
import uvicorn
from fastapi import *
from integrations.integration_wolframalpha import *


app = FastAPI()

@app.get("/api/status")
async def get_api_state():
    return {"api_state": True}

@app.get("/api/general/check_command")
async def general_check_command(sentence):
    answer = IntegrationWolframAlpha.perform_check(sentence)
    if "error" in answer:
        return answer["error"]
    return answer["result"]

if __name__ == "__main__":
    if not os.path.exists("eva-database.db"):
        os.
    uvicorn.run(app, host="0.0.0.0", port=5001)
