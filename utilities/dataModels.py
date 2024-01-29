from pydantic import BaseModel
from utilities.settings import Settings


class CreateUser(BaseModel):
    username: str = ""
    password: str = ""

class ReadUser(BaseModel):
    username: str = ""
    password: str = ""

class UpdateUser(BaseModel):
    userID: str = ""
    username: str = ""
    password: str = ""

class DeleteUser(BaseModel):
    userID: str = ""
    username: str = ""
    password: str = ""

class ReadCommand(BaseModel):
    OSType: str = ""
    command: str = ""
