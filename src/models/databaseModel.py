import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="nibba_clothez"
        )