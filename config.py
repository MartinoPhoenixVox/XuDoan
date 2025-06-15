import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql://root:@localhost/XuDoan")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
