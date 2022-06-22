from ast import literal_eval
from os import environ

from dotenv import load_dotenv

load_dotenv()

DISCORD_GUILD_ID = int(environ.get('DISCORD_GUILD_ID'))
DISCORD_CHANNELS_ID = literal_eval(environ.get('DISCORD_CHANNELS_ID'))

DISCORD_ADMINS = literal_eval(environ.get('DISCORD_ADMINS'))

DISCORD_BOT_TOKEN = environ.get('DISCORD_BOT_TOKEN')

LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO').upper()
