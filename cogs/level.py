import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
from config import DISCORD_GUILD_ID

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="level", description="Affiche le niveau et l'expérience du joueur")
    async def level(self, interaction: discord.Interaction):
        player = self.bot.db.get_player(interaction.user.name)
        if player:
            await interaction.response.send_message(f"Niveau: {player[1]}, Expérience: {player[2]}")
        else:
            await interaction.response.send_message("Joueur non trouvé.")
            
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(level="Nouveau niveau", player_name="Nom du joueur")
    @app_commands.command(name="setlevel", description="Modifie le niveau du joueur")
    async def setlevel(self, interaction: discord.Interaction, level: int, player_name: str = None):
        player_name = player_name or interaction.user.name
        player = self.bot.db.get_player(player_name)
        if player:
            self.bot.db.increment_player_level(player_name)
            await interaction.response.send_message(f"Nouveau niveau: {level}")
        else:
            await interaction.response.send_message("Joueur non trouvé.")
            
    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(exp="Nouvelle expérience", player_name="Nom du joueur")
    @app_commands.command(name="giveexp", description="Ajoute l'expérience au joueur (par défault, l'utilisateur qui utilise la commande)")
    async def giveexp(self, interaction: discord.Interaction, exp: int, player_name: str = None):
        player_name = player_name or interaction.user.name
        player = self.bot.db.get_player(player_name)
        if player:
            self.bot.db.add_experience(player_name, exp)
            await interaction.response.send_message(f"Nouvelle expérience: {exp}")
        else:
            await interaction.response.send_message("Joueur non trouvé.")

    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(player_name="Nom du joueur")
    @app_commands.command(name="remove", description="Supprime un joueur")
    async def remove(self, interaction: discord.Interaction, player_name: str):
        player = self.bot.db.get_player(player_name)
        if player:
            self.bot.db.delete_player(player_name)
            await interaction.response.send_message(f"Joueur {player_name} supprimé.")
        else:
            await interaction.response.send_message("Joueur non trouvé.")

    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="reset", description="Réinitialise les données des joueurs")
    @app_commands.default_permissions(administrator=True)
    async def reset_datas(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Réinitialisation des données", description="Êtes-vous sûr de vouloir réinitialiser toutes les données des membres ?", color=discord.Color.red())
        yes_button = Button(label="Oui", style=discord.ButtonStyle.green)
        no_button = Button(label="Non", style=discord.ButtonStyle.red)
        view = View(timeout=60)
        
        async def yes_callback(interaction: discord.Interaction):
            self.bot.db.reset_database()
            await interaction.response.send_message("Base de données réinitialisée.", embed=None, view=None)
            await interaction.delete_original_response()
            view.stop()
            
        async def no_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Réinitialisation annulée.", embed=None, view=None)
            await interaction.delete_original_response()
            view.stop()
            
        yes_button.callback = yes_callback
        no_button.callback = no_callback
        
        view.add_item(yes_button)
        view.add_item(no_button)
        
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.guilds(discord.Object(id=DISCORD_GUILD_ID))
    @app_commands.command(name="leaderboard", description="Affiche le classement des joueurs")
    async def leaderboard(self, interaction: discord.Interaction):
        leaderboard = self.bot.db.get_leaderboard()
        if leaderboard:
            embed = discord.Embed(title="Classement des joueurs", color=discord.Color.blue())
            for i, (name, level, exp) in enumerate(leaderboard, start=1):
                embed.add_field(name=f"{i}. {name}", value=f"Niveau: {level}, Expérience: {exp}", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Aucun joueur trouvé.")
            
    

async def setup(bot):
    await bot.add_cog(Level(bot))