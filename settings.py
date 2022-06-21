from os import environ

from dotenv import load_dotenv
from ast import literal_eval

load_dotenv()

DB_URL = environ.get('DATABASE_URL')
DB_NAME = environ.get('DB_NAME')
DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_HOST = environ.get('DB_HOST')
if DB_URL is None:
    DB_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

DISCORD_GUILD_ID = int(environ.get('DISCORD_GUILD_ID'))
DISCORD_CHANNEL_ID = int(environ.get('DISCORD_CHANNEL_ID'))

DISCORD_ADMINS = literal_eval(environ.get('DISCORD_ADMINS'))

DISCORD_BOT_TOKEN = environ.get('DISCORD_BOT_TOKEN')

LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO').upper()
