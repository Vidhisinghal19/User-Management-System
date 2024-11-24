#ums/app/db.py
import mysql.connector
import os

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'db'),
            user=os.getenv('MYSQL_USER', 'vidhi'),
            password=os.getenv('MYSQL_PASSWORD', '1234'),
            database=os.getenv('MYSQL_DATABASE', 'ums')
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
