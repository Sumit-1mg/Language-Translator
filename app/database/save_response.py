import os
import sqlite3
from datetime import datetime

class StoreTranslationResponse:

    #path_to_database = os.path.dirname(os.path.dirname(os.getcwd()))+'/database.db'
    path_to_database = os.getcwd() + '/database.db'

    @classmethod
    def create_table(cls):
        # Connect to the database and create the 'translation_requests' table if it doesn't exist
        with sqlite3.connect(cls.path_to_database) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translation_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    api_used TEXT NOT NULL,
                    translation_success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            ''')
            conn.commit()


    @classmethod
    def store_translation_request(cls,source_language, target_language, api_used, translation_success):
        # Insert the translation request data into the 'translation_requests' table
        try:
            cls.create_table()
            timestamp = datetime.utcnow()
            with sqlite3.connect(cls.path_to_database) as conn:

                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO translation_requests (source_language, target_language, api_used, translation_success, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (source_language, target_language, api_used, int(translation_success), timestamp))
                conn.commit()

        except Exception as e:
            print("Error: ", str(e))
