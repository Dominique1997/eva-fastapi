from pydantic import BaseModel
from utilities.settings import Settings


class Token(BaseModel):
    token: str = ""

class CreateUser(Token):
    username: str = ""
    password: str = ""

class ReadUser(Token):
    userID: str = ""
    username: str = ""
    password: str = ""

class UpdateUser(Token):
    username: str = ""
    password: str = ""

class DeleteUser(Token):
    username: str = ""
    password: str = ""

class ReadCommand(Token):
    OSType: str = ""
    command: str = ""
