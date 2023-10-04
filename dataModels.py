from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

class Login_query(BaseModel):
    login_query: str

