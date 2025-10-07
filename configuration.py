import os
from local_settings import *


class Configuration:
    SECRET_KEY = SECRET_KEY
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False