import sqlite3
import os

DB_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage.db")

class StorageDriver:
    def __init__(self, path: str = DB_FILE_PATH):  
        self.conn = sqlite3.connect(path)
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    name TEXT PRIMARY KEY,
                    value INTEGER,
                    UNIQUE(name)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    difficulty TEXT PRIMARY KEY,
                    value INTEGER,
                    UNIQUE(difficulty)
                )
            """)
    
    def get_setting(self, name: str, default: bool) -> bool:
        cursor = self.conn.execute("""
            SELECT value FROM settings WHERE name = ?
        """, (name,))
        result = cursor.fetchone()
        return default if result == None else bool(result[0])
        
    def set_setting(self, name: str, value: bool):
        val = 1 if value else 0
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO settings (name, value) VALUES (?, ?)
            """, (name, val))

    def get_difficulty_record(self, difficulty: int):
        cursor = self.conn.execute("""
            SELECT value FROM records WHERE difficulty = ?
        """, (difficulty,))
        result = cursor.fetchone()
        return 0 if result == None else int(result[0])

    def set_difficulty_record(self, difficulty: int, value: int):
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO records (difficulty, value) VALUES (?, ?)
            """, (difficulty, value))
    
    def close(self):
        self.conn.close()
        
    def __del__(self):
        self.close()