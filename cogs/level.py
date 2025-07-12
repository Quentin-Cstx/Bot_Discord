import discord
from discord.ext import commands, tasks
from discord import app_commands
from config import DISCORD_GUILD_ID, DISCORD_CHANNEL_ID_QUOTE_OF_THE_DAY

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
    @app_commands.command(name="setexp", description="Ajoute l'expérience au joueur (par défault, l'utilisateur qui utilise la commande)")
    async def addexp(self, interaction: discord.Interaction, exp: int, player_name: str = None):
        player_name = player_name or interaction.user.name
        player = self.bot.db.get_player(player_name)
        if player:
            self.bot.db.add_experience(player_name, exp)
            await interaction.response.send_message(f"Nouvelle expérience: {exp}")
        else:
            await interaction.response.send_message("Joueur non trouvé.")


async def setup(bot):
    await bot.add_cog(Level(bot))