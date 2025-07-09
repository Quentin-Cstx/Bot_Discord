import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from discord import app_commands
from config import DISCORD_GUILD_ID
import aiohttp


class Commandesapi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="quote", description="Affiche une citation aléatoire")
    async def quote(self, interaction: discord.Interaction):
        api_url = "https://zenquotes.io/api/random"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    await interaction.response.send_message("Erreur lors de la récupération de la citation.", ephemeral=True)
                    return
                data = await response.json()
        embed = discord.Embed(title="Citation", color=discord.Color.blue())
        embed.add_field(name=data[0]['q'], value=data[0]['a'], inline=False)
        embed.set_footer(text="Source: https://zenquotes.io")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Commandesapi(bot))