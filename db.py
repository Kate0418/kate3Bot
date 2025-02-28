import pymysql
import os
from dotenv import load_dotenv

def db(sql, params):
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306))  # デフォルトで3306
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )
    cursor = conn.cursor()

    cursor.execute(sql, params)

    conn.commit()
    result = cursor.fetchall()

    return result
