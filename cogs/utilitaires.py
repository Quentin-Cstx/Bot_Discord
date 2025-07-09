import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from discord import app_commands
from config import DISCORD_GUILD_ID

class Utilitaires(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="ping", description="Répond si le bot est en ligne")
    async def ping(self, interaction: discord.Interaction):
        """
        Commande : /ping
        
        Cette commande permet de vérifier si le bot est en ligne et répond.

        Réponse :
        - La commande répondra avec un message indiquant que le bot est en ligne.
        """
        await interaction.response.send_message("Je suis en ligne !")
        
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="info", description="Affiche des informations sur le bot")
    async def info(self, interaction: discord.Interaction):
        """
        Commande : /info
        
        Cette commande affiche des informations sur le bot, telles que son nom, son ID, le nombre de serveurs et d'utilisateurs.

        Réponse :
        - La commande répondra avec un embed contenant les informations du bot.
        """
        embed = discord.Embed(title="Informations sur le Bot", color=discord.Color.blue())
        embed.add_field(name="Nom", value=self.bot.user.name, inline=True)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Serveurs", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Utilisateurs", value=len(set(self.bot.get_all_members())), inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID)) 
    @app_commands.command(name="help", description="Affiche la liste des commandes disponibles")
    async def help_command(self, interaction: discord.Interaction):
        """
        Commande : /help
        
        Cette commande affiche une liste des commandes disponibles pour le bot.

        Réponse :
        - La commande répondra avec un embed contenant la liste des commandes disponibles.
        """
        embed = discord.Embed(title="Commandes Disponibles", color=discord.Color.green())
        embed.add_field(name="/ping", value="Vérifie si le bot est en ligne.", inline=False)
        embed.add_field(name="/info", value="Affiche des informations sur le bot.", inline=False)
        embed.add_field(name="/help", value="Affiche cette liste de commandes.", inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    
async def setup(bot):
    await bot.add_cog(Utilitaires(bot))
