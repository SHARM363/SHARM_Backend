import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "sharm_secret_key")

    DATABASE_URL = os.getenv("DATABASE_URL")

    BOT_TOKEN = os.getenv("BOT_TOKEN")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
