import os

class Config:
    SECRET_KEY = "change_this_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///chat.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5050   # ✅ 不用 8000