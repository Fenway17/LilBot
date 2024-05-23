import sqlite3
import os
from typing import Optional

DATABASE_FILE_PATH = "../../sqlite/user_database.db"


class SQLiteDatabase:
    _instance: Optional["SQLiteDatabase"] = None

    def __new__(cls, db_name: str = DATABASE_FILE_PATH):
        if cls._instance is None:
            cls._instance = super(SQLiteDatabase, cls).__new__(cls)
            cls._instance._initialize(db_name)
        return cls._instance

    def _initialize(self, db_name: str):
        # Ensure the directory exists
        db_dir = os.path.dirname(db_name)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):  # only creates a table if it does not exist in the file
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS registered_users (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL
                              )"""
        )
        self.connection.commit()

    def register_user(self, user_id: int, username: str):
        self.cursor.execute(
            "INSERT OR REPLACE INTO registered_users (user_id, username) VALUES (?, ?)",
            (user_id, username),
        )
        self.connection.commit()

    def deregister_user(self, user_id: int):
        self.cursor.execute(
            "DELETE FROM registered_users WHERE user_id = ?", (user_id,)
        )
        self.connection.commit()

    def user_is_registered(self, user_id: int) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM registered_users WHERE user_id = ?", (user_id,)
        )
        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()
