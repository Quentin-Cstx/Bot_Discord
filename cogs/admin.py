"""
Admin cog for Discord bot, providing admin-only commands and error handling.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from discord import app_commands
from config import DISCORD_GUILD_ID

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="secret", description="Commande réservée aux admins")
    async def secret_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Tu es admin, accès accordé !")
        
        
        
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="clear", description="Supprimer des messages dans un salon")
    @app_commands.describe(amount="Nombre de messages à supprimer")
    async def clear(self, interaction: discord.Interaction, amount: int):
        """
        Commande : /clear
        
        Cette commande permet de supprimer un certain nombre de messages dans le salon actuel.

        Paramètres :
        - `amount` : Le nombre de messages à supprimer (doit être un entier positif).

        Permissions requises :
        - L'utilisateur doit avoir la permission de gérer les messages dans le salon.

        Réponse :
        - La commande répondra avec un message indiquant le nombre de messages supprimés.
        """
        await interaction.response.defer(ephemeral=True)  # Diffère la réponse AVANT purge
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 {len(deleted)} messages supprimés.", ephemeral=True)

    
    
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="lock", description="Verrouiller un salon")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        """
        Commande : /lock
        
        Cette commande permet de verrouiller le salon actuel, empêchant les utilisateurs de poster des messages.

        Permissions requises :
        - L'utilisateur doit avoir la permission de gérer les salons dans le serveur.

        Réponse :
        - La commande répondra avec un message indiquant que le salon a été verrouillé.
        """
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔒 Salon verrouillé.")



    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="unlock", description="Déverrouiller un salon")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        """
        Commande : /unlock
        
        Cette commande permet de déverrouiller le salon actuel, permettant aux utilisateurs de poster des messages.

        Permissions requises :
        - L'utilisateur doit avoir la permission de gérer les salons dans le serveur.

        Réponse :
        - La commande répondra avec un message indiquant que le salon a été déverrouillé.
        """
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("🔓 Salon déverrouillé.")
    
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="togglefeur", description="Active ou désactive la réponse 'FEUR' pour les messages")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(toggle="Activer ou désactiver la réponse 'FEUR'")
    async def togglefeur(self, interaction: discord.Interaction, toggle: bool):
        """
        Commande : /togglefeur
        
        Cette commande permet d'activer ou de désactiver la réponse "FEUR" pour les messages contenant "quoi" ou "quoi?".

        Paramètres :
        - `toggle` : Un booléen pour activer (True) ou désactiver (False) la réponse "FEUR".

        Permissions requises :
        - L'utilisateur doit avoir la permission d'administrateur dans le serveur.

        Réponse :
        - La commande répondra avec un message indiquant si la réponse "FEUR" est activée ou désactivée.
        """
        self.bot.toggle_feur = toggle
        status = "activée" if toggle else "désactivée"
        await interaction.response.send_message(f"Réponse 'FEUR' {status}.", ephemeral=True)
        
    
    
    
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="shutdown", description="Éteindre le bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def shutdown(self, interaction: discord.Interaction):
        """
        Commande : /shutdown
        
        Cette commande permet d'éteindre le bot.

        Permissions requises :
        - L'utilisateur doit avoir la permission d'administrateur dans le serveur.

        Réponse :
        - La commande répondra avec un message indiquant que le bot s'éteint.
        """
        await interaction.response.send_message("🔌 Bot en cours d'arrêt...")
        await self.bot.close()


                
async def setup(bot):
    """Adds the Admin cog to the bot."""
    await bot.add_cog(Admin(bot))
