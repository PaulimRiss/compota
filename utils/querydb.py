import sqlite3
from os import environ
from dotenv import load_dotenv

load_dotenv()


def execute(query, params=None):
    conn = sqlite3.connect(environ.get("DATABASE_PATH"))
    cursor = conn.cursor()

    if params is not None:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data
