from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

class LoginQuery(BaseModel):
    login_query: str

class CheckQuery(LoginQuery):
    sentence: str
    program_type: str

class NewUser(LoginQuery):
    username: str
    password: str
class UpdateUserGeneral(LoginQuery):
    userid: int
    new_username: str
    new_password: str
class UpdateUserName(LoginQuery):
    userid: int
    new_username: str

class UpdateUserPassword(LoginQuery):
    userid: int
    new_password: str

class DeleteUser(LoginQuery):
    userid: int

class SelectUser(LoginQuery):
    program_type: str
    username: str
    password: str
    discord_name: str

class AddToken(LoginQuery):
    userID: int
    server_ip: str
    server_port: str
    server_username: str
    server_password: str
    server_token: str

class UpdateTokenGeneral(LoginQuery):
    tokenID: int
    userID: int
    server_ip: str
    server_port: str
    server_username: str
    server_password: str
    server_token: str

class UpdateTokenServerIP(LoginQuery):
    tokenID: int
    userID: int
    server_ip: str

class UpdateTokenServerPort(LoginQuery):
    tokenID: int
    userID: int
    server_port: str

class UpdateServerUsername(LoginQuery):
    tokenID: int
    userID: int
    server_username: str

class UpdateServerUserPassword(LoginQuery):
    tokenID: int
    userID: int
    server_password: str

class UpdateServerToken(LoginQuery):
    tokenID: int
    userID: int
    server_token: str

class SelectServerToken(LoginQuery):
    tokenid: int
    userid: int

class DeleteServerToken(LoginQuery):
    tokenid: int
    userid: int