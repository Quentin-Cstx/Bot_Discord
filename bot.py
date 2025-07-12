import discord
from discord.ext import commands
import os
import asyncio
import re

from config import TOKEN, DISCORD_GUILD_ID
from data_joueurs import Database as DataJoueurs


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

db = DataJoueurs()
bot.db = db

@bot.event
async def on_ready():
    print(f"Connecte en tant que {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
        print(f"{len(synced)} slash command(s) synchronisee(s)")
    except Exception as e:
        print(f"Erreur de sync: {e}")



@bot.event
async def on_message(message):
    author = message.author
    if author == bot.user:
        return
    print(f"Message de {author.name}: {message.content}")
    if bot.db.get_player(author.name) is None:
        print(f"Joueur {author.name} non trouve, ajout avec niveau 1.")
        bot.db.add_player(author.name, 1)
        print(f"Joueur {author.name} ajoute avec le niveau 1.")
    else:
        bot.db.add_experience(author.name, 10)
    
    content_lower = message.content.lower().strip()
    if re.search(r"quoi\??\s*$", content_lower):
        await message.reply("FEUR!")
    await bot.process_commands(message)


async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Extension loaded: cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension cogs.{filename[:-3]}: {e}")

async def main():
    await load_extensions()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
