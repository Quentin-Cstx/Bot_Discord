
import discord
from discord.ext import commands, tasks
from discord import app_commands
from config import DISCORD_GUILD_ID, DISCORD_CHANNEL_ID_QUOTE_OF_THE_DAY
import aiohttp


class CommandesApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(hours=24)
    async def quoteOfTheDay(self):
        api_url = "https://zenquotes.io/api/today"
        channel = self.bot.get_channel(DISCORD_CHANNEL_ID_QUOTE_OF_THE_DAY)
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    print("Erreur lors de la récupération de la citation.")
                    return
                data = await response.json()
        embed = discord.Embed(title="Citation du jour", color=discord.Color.blue())
        embed.add_field(name=data[0]['q'], value=data[0]['a'], inline=False)
        embed.set_footer(text="Source: https://zenquotes.io")
        await channel.send(embed=embed)
    
    @quoteOfTheDay.before_loop
    async def before_quoteOfTheDay(self):
        await self.bot.wait_until_ready()
    
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
    cog = CommandesApi(bot)
    cog.quoteOfTheDay.start()
    await bot.add_cog(cog)