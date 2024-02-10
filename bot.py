import logging
import os

import discord
from supabase import create_client, Client

from discord.ext import commands
from cogs.scraper import Scraper
from cogs.tournaments import Tournament

class Bot(commands.Bot):
    def __init__(self, guild_id: int, intents: discord.Intents, supabase_client: Client):
        super().__init__('$',intents=intents)
        self.guild_id = guild_id
        self.supabase: Client = supabase_client

    async def on_ready(self):
        self.tree.on_error = self.on_tree_error
        logging.info("We are ready to rumble!")

        # await self.tree.sync()
    async def setup_hook(self):
        logging.info('Loading cogs')
        await self.add_cog(Scraper(self))
        await self.add_cog(Tournament(self))

    async def on_tree_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!", ephemeral=True)
        elif isinstance(error, discord.app_commands.MissingRole):
            return await interaction.response.send_message(f"You're missing permissions to use that", ephemeral=True)
        else:
            raise error
