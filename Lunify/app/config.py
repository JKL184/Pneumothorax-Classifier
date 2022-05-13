import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = False
    #SECRET_KEY = "lungify"
    UPLOAD_FOLDER = './app/static/uploads'
    OUTPUT_FOLDER = './app/static/outputs'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://lungify:lungify@localhost/lungify_db'
    #DATABASE_URL='postgresql://lungify:lungify@localhost/lungify_db'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed