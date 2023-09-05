import jwt
import sqlite3
from settings import Settings

class Database:

    key = Settings.get_encryption_key()
    algorithm = Settings.get_algorithm()
    @classmethod
    def new_database_setup(cls):
        with sqlite3.connect("eva-database.db") as db:
            create_new_table_users_statement = 'CREATE TABLE "users" (\
                "userid"	INTEGER NOT NULL,\
                "username"	TEXT NOT NULL,\
                "password"	TEXT,\
                "discord_username"	TEXT,\
                PRIMARY KEY("userid" AUTOINCREMENT)\
                )'
            create_new_table_tokens_statement = 'CREATE TABLE "tokens" (\
                "tokenid"	INTEGER NOT NULL,\
                "server_ip"	TEXT NOT NULL,\
                "server_port"	TEXT NOT NULL,\
                "server_username"	TEXT,\
                "server_password"	TEXT,\
                "server_token"	TEXT NOT NULL,\
                PRIMARY KEY("tokenid" AUTOINCREMENT)\
                )'
            db.execute(create_new_table_users_statement)
            db.execute(create_new_table_tokens_statement)
    @classmethod
    def create_new_user(cls, username, password):
        with sqlite3.connect("eva-database.db") as db:
            create_new_user_statement = f'INSERT INTO users(username,password) VALUES("{username}","{password}")'
            answer_creation_user = db.execute(create_new_user_statement)
            print(answer_creation_user.rowcount)
            if answer_creation_user.rowcount > 0:
                return {"confirmation": "User has been created"}
            return {"error": "User could not be created"}

    @classmethod
    def delete_user(cls, userid):
        with sqlite3.connect("eva-database.db") as db:
            remove_user_statement = f"DELETE FROM users WHERE userid == {userid}"
            answer_removing_user = db.execute(remove_user_statement)
            print(answer_removing_user.rowcount)
            if answer_removing_user.rowcount > 0:
                return {"confirmation": "User has been removed"}
            return {"error": "User could not be removed"}

    @classmethod
    def update_user(cls, userid, new_username, new_password):
        with sqlite3.connect("eva-database.db") as db:
            update_user_statement = f'UPDATE users SET username="{new_username}", password="{new_password}" WHERE userid="{userid}"'
            answer_updating_user = db.execute(update_user_statement)
            if answer_updating_user.rowcount > 0:
                return {"confirmation": "User has been updated"}
            return {"error": "User could not be updated"}


    @classmethod
    def select_user(cls, program_type, username, password, discord_username):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            if program_type != "discord":
                select_user_statement = f'SELECT * FROM users WHERE username = "{username}" AND password = "{password}"'
            else:
                select_user_statement = f'SELECT * FROM users WHERE discord_username = "{discord_username}"'
            db_data = db_cursor.execute(select_user_statement).fetchall()
            print(db_cursor.execute(select_user_statement).rowcount)
            if len(db_data) > 1 or len(db_data) == 0:
                return {"Login_state": "login_error", "Message": "User not found"}
            return {"Login_state": "logged_in", "Message": "User is found"}

    #RETURN STATE NEEDS TO BE UPDATED
    @classmethod
    def add_user_token(cls, userid, server_ip, server_port, server_username, server_password, server_token):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            add_user_token_statement = f"INSERT INTO tokens(userID, server_ip, server_port, server_username, server_password, server_token)" \
                      f"VALUES('{userid}','{server_ip}',' {server_port}', '{server_username}', '{server_password}'," \
                      f"'{server_token}')"
            print(db_cursor.execute(add_user_token_statement).rowcount)
    @classmethod
    def update_user_token(cls, tokenid, userid, server_ip, server_port, server_username, server_password, server_token):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            add_user_token_statement = f'UPDATE tokens ' \
                                       f'SET server_ip="{server_ip}",' \
                                       f'server_port="{server_port}",' \
                                       f'server_username="{server_username}",' \
                                       f'server_password="{server_password}",' \
                                       f'server_token="{server_token}"' \
                                       f'WHERE userID="{userid}" and tokenid="{tokenid}"'
            print(db_cursor.execute(add_user_token_statement).rowcount)

    @classmethod
    def delete_user_token(cls, tokenid, userid):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            add_user_token_statement = f"DELETE FROM tokens WHERE userid == {userid} and tokenid == {tokenid}"
            print(db_cursor.execute(add_user_token_statement).rowcount)

    @classmethod
    def select_user_token(cls, tokenid, userid):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            add_user_token_statement = f'SELECT * FROM tokens ' \
                                       f'WHERE userID="{userid}" and tokenid="{tokenid}"'
            print(db_cursor.execute(add_user_token_statement).rowcount)