import os

SECRET_KEY = os.getenv('SECRET_KEY') or 'secret'
DEBUG = os.getenv("DEBUG") or False

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "mysql://username:password@host:port/database_name"
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") or False
