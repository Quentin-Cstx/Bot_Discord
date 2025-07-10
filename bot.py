from config import TOKEN, DISCORD_GUILD_ID
import discord
from discord.ext import commands
import os


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecte en tant que {bot.user}")
    try:
        synced = await bot.tree.sync(guild = discord.Object(id=DISCORD_GUILD_ID))
        print(f"{len(synced)} slash command(s) synchronisee(s)")
    except Exception as e:
        print(f"Erreur de sync: {e}")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()
    if content_lower.endswith("quoi") or content_lower.endswith("quoi?"):
        await message.reply("FEUR!")
    await bot.process_commands(message)



async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load_extensions()   
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
