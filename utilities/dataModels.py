from pydantic import BaseModel
from utilities.settings import Settings


class Token(BaseModel):
    token: str = ""


class User(Token):
    username: str
    password: str

class CreateUser(User):
    User.username = ""
    User.password = ""

class ReadUser(User):
    User.username = ""
    User.password = ""

class UpdateUser(User):
    User.username = ""
    User.password = ""
    userId: str = "0"

class DeleteUser(User):
    User.username = ""
    User.password = ""
    userId: str = "0"
