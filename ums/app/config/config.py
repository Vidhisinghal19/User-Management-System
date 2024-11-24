#ums/app/config/config.py
import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'vidhi')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'ums')
