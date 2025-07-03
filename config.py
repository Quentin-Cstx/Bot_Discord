import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
