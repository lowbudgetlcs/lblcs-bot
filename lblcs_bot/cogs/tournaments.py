import discord, discord.ext.commands as commands
from discord import app_commands
import logging

def check_code_role(interaction: discord.Interaction) -> bool:
    # accepted_roles = ["Captain", "Admin", "Sub-Team-Lead", "Dev"]
    # return True in [(x in accepted_roles) for x in interaction.user.roles]
    return True

class Tournament(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Tournament cog")
        self.bot = bot
        self.tournaments = []

    @app_commands.command(name='tcode')
    @app_commands.check(check_code_role)
    async def tcode(self, interaction: discord.Interaction):
        # TODO: Hit RIOT API endpoint to generate tcode
        await interaction.response.send_message("Hello, world!")