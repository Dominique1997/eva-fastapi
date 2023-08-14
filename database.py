import jwt
import sqlite3

class Database():
    db = sqlite3.connect("eva-database.db")
    key = "testing"
    algorithm = "HS256"
    @classmethod
    def new_database_setup(cls):
        create_new_table_users_statement = 'CREATE TABLE "users" (\
        	"userid"	INTEGER NOT NULL,\
        	"username"	TEXT NOT NULL,\
        	"password"	TEXT,\
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
    @classmethod
    def create_new_user(cls, username, password):
        pass
    @classmethod
    def delete_user(cls, username, password):
        pass

    @classmethod
    def update_user(cls, username, password):
        pass

    @classmethod
    def select_user(cls, query_information):
        decoded = jwt.decode(query_information, key="testing", algorithms=["HS256"])
        username = decoded["username"]
        password = decoded["password"]
        db_cursor = cls.db.cursor()
        command = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        db_data = db_cursor.execute(command).fetchall()
        if len(db_data) > 1 or len(db_data) == 0:
            return {"Login_state": "login_error", "Message": "User not found"}
        return {"Login_state": "logged_in", "Message": "User is found", "username": username, "password": password}
