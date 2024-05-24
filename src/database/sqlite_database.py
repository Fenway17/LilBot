import sqlite3
import os
from typing import Optional

DATABASE_FILE_PATH = "sqlite/user_database.db"

valid_roles = [
    "user",
    "master",
    "developer",
]


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
        print(f"Database will be stored at: {db_dir}")  # show in terminal the directory

        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):  # only creates a table if it does not exist in the file
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS registered_users (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                user_role TEXT DEFAULT 'user'
                              )"""
        )
        self.connection.commit()

    def register_user(self, user_id: int, username: str, role: str = "user"):
        self.cursor.execute(
            "INSERT OR REPLACE INTO registered_users (user_id, username, user_role) VALUES (?, ?, ?)",
            (user_id, username, role),
        )
        self.connection.commit()

    def deregister_user(self, user_id: int):
        self.cursor.execute(
            "DELETE FROM registered_users WHERE user_id = ?", (user_id,)
        )
        self.connection.commit()

    def is_user_registered(self, user_id: int) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM registered_users WHERE user_id = ?", (user_id,)
        )
        return self.cursor.fetchone() is not None

    def update_user_role(self, user_id: int, role: str):
        # last resort guard to prevent adding of invalid roles, check in bot commands instead
        if role not in valid_roles:
            return

        self.cursor.execute(
            "UPDATE registered_users SET user_role = ? WHERE user_id = ?",
            (role, user_id),
        )
        self.connection.commit()

    def get_user_role(self, user_id: int) -> Optional[str]:
        self.cursor.execute(
            "SELECT user_role FROM registered_users WHERE user_id = ?", (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def user_has_role(self, user_id: int, role: str) -> bool:
        user_role = self.get_user_role(user_id)
        return user_role == role

    def close(self):
        self.connection.close()
