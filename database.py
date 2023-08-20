import jwt
import sqlite3


class Database():

    key = "testing"
    algorithm = "HS256"
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
            if answer_creation_user.lastrowid > 0:
                return {"confirmation": "User has been created"}
            return {"error": "User could not be created"}

    @classmethod
    def delete_user(cls, username, password):
        with sqlite3.connect("eva-database.db") as db:
            pass

    @classmethod
    def update_user(cls, userid, new_username, new_password):
        with sqlite3.connect("eva-database.db") as db:
            update_user_statement = f'UPDATE users SET username="{new_username}", password="{new_password}" WHERE userid="{userid}"'
            answer_updating_user = db.execute(update_user_statement)
            if answer_updating_user.lastrowid > 0:
                return {"confirmation": "User has been updated"}
            return {"error": "User could not be updated"}


    @classmethod
    def select_user(cls, program_type, username, password, discord_username):
        with sqlite3.connect("eva-database.db") as db:
            db_cursor = db.cursor()
            if program_type != "discord":
                command = f'SELECT * FROM users WHERE username = "{username}" AND password = "{password}"'
            else:
                command = f'SELECT * FROM users WHERE discord_username = "{discord_username}"'
            db_data = db_cursor.execute(command).fetchall()
            if len(db_data) > 1 or len(db_data) == 0:
                return {"Login_state": "login_error", "Message": "User not found"}
            return {"Login_state": "logged_in", "Message": "User is found"}
