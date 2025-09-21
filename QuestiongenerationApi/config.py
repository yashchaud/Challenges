import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'our-secret'
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'jwt-secret-key'
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRY_HOURS = 24

    # db stuff
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    DB_NAME = os.environ.get('DB_NAME') or 'question_api'