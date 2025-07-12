import discord
from discord.ext import commands
from discord import app_commands
from config import DISCORD_GUILD_ID
import aiohttp

class ValorantApi(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="agent", description="Affiche des informations sur l'agent choisit")
    @app_commands.describe(agent="Nom de l'agent", language="Langue de la réponse")
    @app_commands.choices(language=[
        app_commands.Choice(name="Français", value="fr-FR"),
        app_commands.Choice(name="Anglais", value="en-US"),
        app_commands.Choice(name="Espagnol", value="es-ES"),
        app_commands.Choice(name="Allemand", value="de-DE")
    ])
    async def agent(self, interaction: discord.Interaction, agent: str, language: str = "fr-FR"):
        api_url = f"https://valorant-api.com/v1/agents?search={agent}&language={language}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    await interaction.response.send_message("Erreur lors de la récupération des informations sur l'agent.", ephemeral=True)
                    return
                data = await response.json()
        
        if not data['data']:
            await interaction.response.send_message(f"Aucun agent trouvé avec le nom '{agent}'.", ephemeral=True)
            return
        for data in data['data']:
            if data['displayName'].lower() == agent.lower():
                agent_data = data
                break
        else:
            await interaction.response.send_message(f"Aucun agent trouvé avec le nom '{agent}'.", ephemeral=True)
            return
        # Création de l'embed avec les informations de l'agent
        embed = discord.Embed(title=agent_data['displayName'], color=discord.Color.blue())
        embed.add_field(name="Rôle", value=agent_data['role']['displayName'], inline=True)
        embed.add_field(name="Description", value=agent_data['description'], inline=False)
        embed.set_thumbnail(url=agent_data['displayIcon'])
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(ValorantApi(bot))