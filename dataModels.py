from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

