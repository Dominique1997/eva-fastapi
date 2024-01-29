import sqlite3
from utilities.settings import Settings

class IntegrationDatabase:
    key = Settings.get_encryption_key()
    algorithm = Settings.get_algorithm()
    sql_server_ip = Settings.get_sql_server_ip()
    sql_server_port = Settings.get_sql_server_port()
    sql_server_username = Settings.get_sql_server_username()
    sql_server_password = Settings.get_sql_server_password()
    sql_server_database_name = Settings.get_sql_server_database_name()

    db = sqlite3.connect("eva_database.db")
    @classmethod
    def new_database_setup(cls):
        create_new_table_users_statement = 'CREATE TABLE IF NOT EXISTS "users" (\
            "userid"	INTEGER NOT NULL,\
            "username"	TEXT NOT NULL,\
            "password"	TEXT,\
            PRIMARY KEY("userid" AUTOINCREMENT)\
            )'
        create_new_table_tokens_statement = 'CREATE TABLE IF NOT EXISTS "tokens" (\
            "tokenid"	INTEGER NOT NULL,\
            "server_ip"	TEXT NOT NULL,\
            "server_port"	TEXT NOT NULL,\
            "server_username"	TEXT,\
            "server_password"	TEXT,\
            "server_token"	TEXT NOT NULL,\
            PRIMARY KEY("tokenid" AUTOINCREMENT)\
            )'
        cls.db.cursor().execute(create_new_table_users_statement)
        cls.db.execute(create_new_table_tokens_statement)

    @classmethod
    def create_new_user(cls, new_username, new_password):
        create_new_user_statement = f"INSERT INTO users(username,password) VALUES ('{new_username}', '{new_password}')"
        return cls._perform_sql_command(create_new_user_statement).rowcount

    @classmethod
    def read_existing_user(cls, read_username, read_password):
        read_existing_user_statement = f"SELECT userid FROM users WHERE username='{read_username}' and password='{read_password}'"
        return cls._perform_sql_command(read_existing_user_statement).fetchone()

    @classmethod
    def update_existing_user(cls, userId, new_username, new_password):
        update_existing_user_statement = f"UPDATE users SET username='{new_username}', password='{new_password}' WHERE userid='{userId}'"
        return cls._perform_sql_command(update_existing_user_statement).rowcount

    @classmethod
    def delete_existing_user(cls, userId, username, password):
        delete_existing_user_statement = f"DELETE FROM users WHERE userid={userId} and username='{username}' and password='{password}'"
        return cls._perform_sql_command(delete_existing_user_statement).rowcount

    @classmethod
    def reset_tables(cls):
        drop_table_users = "DROP table users"
        cls._perform_sql_command(drop_table_users)
        drop_table_tokens = "DROP table tokens;"
        cls._perform_sql_command(drop_table_tokens)
        cls.new_database_setup()

    @classmethod
    def _perform_sql_command(cls, sql_command):
        db_result = cls.db.execute(sql_command)
        cls.db.commit()
        return db_result
