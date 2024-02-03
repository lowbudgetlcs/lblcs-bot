import discord
from discord import app_commands
from discord.ext import commands
import logging

class Scraper(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading scraper cog")
        self.bot = bot

    @app_commands.command()
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, world!")