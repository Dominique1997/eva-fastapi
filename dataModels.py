from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class query(BaseModel):
    queryString: str

class checkCommand(query):
    command: str