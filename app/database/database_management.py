import sqlite3
from datetime import datetime

DATABASE_FILE = "/Users/sumit.gangwar1/Desktop/Language-Translator/database.db"


def create_table():
    # Connect to the database and create the 'translation_requests' table if it doesn't exist
    with sqlite3.connect(DATABASE_FILE) as conn:
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


def insert_translation_request(source_language, target_language, api_used, translation_success):
    # Insert the translation request data into the 'translation_requests' table
    try:
        create_table()
        timestamp = datetime.utcnow()
        with sqlite3.connect(DATABASE_FILE) as conn:

            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO translation_requests (source_language, target_language, api_used, translation_success, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (source_language, target_language, api_used, int(translation_success), timestamp))
            conn.commit()
        print("data inserted successfully")

    except:
        print("Error while inserting data in database")
