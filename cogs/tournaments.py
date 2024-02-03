import discord, discord.ext.commands as commands
from discord import app_commands
import logging
from supabase import create_client, Client
import os
from modals.GameCreationModal import GameCreationModal

def check_code_role(interaction: discord.Interaction) -> bool:
    accepted_roles = ["Captain", "Admin", "Sub-Team-Lead", "Dev"]
    authorized = [(x.name in accepted_roles) for x in interaction.user.roles]
    return True in authorized

class Tournament(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Tournament cog")
        self.bot = bot
        self.tournaments = []
        self.supabase = bot.supabase

    @app_commands.command(name='generate-tournament-code', description="Used to generate a tournament code!")
    @app_commands.check(check_code_role)
    async def tcode(self, interaction: discord.Interaction):
        logging.info("Code generation invoked")

        await interaction.response.send_modal(GameCreationModal(self.supabase))
