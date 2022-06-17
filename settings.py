from os import environ

from dotenv import load_dotenv

load_dotenv()

DB_URL = environ.get('DATABASE_URL')
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_HOST = environ.get("DB_HOST")

LOG_LEVEL = environ.get("LOG_LEVEL", "INFO").upper()

DISCORD_BOT_TOKEN = environ.get("DISCORD_BOT_TOKEN")
