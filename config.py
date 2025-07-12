import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
DISCORD_CHANNEL_ID_QUOTE_OF_THE_DAY = int(os.getenv("DISCORD_CHANNEL_ID_QUOTE_OF_THE_DAY"))
