import logging
import os
from supabase import create_client, Client

from discord.ext import commands
import lblcs_bot.models
from lblcs_bot.cogs.scraper import Scraper
from lblcs_bot.cogs.tournaments import Tournament


class Bot(commands.Bot):
    def __init__(self,guild_id,intents):
        super().__init__('$',intents=intents)
        self.guild_id = guild_id
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    async def on_ready(self):
        logging.info(f'Logged in as {self.user} GUILD_ID: {self.guild_id}')
        # guild = self.get_guild(self.guild_id)
        # print(f'{guild}')
        # members = guild.members
        # for member in members:
        #     print(f'{member.roles}')
        logging.info("Syncing application commands")
        await self.tree.sync(guild=self.get_guild(self.guild_id))

    async def setup_hook(self):
        logging.info('Loading cogs')
        await self.add_cog(Tournament(self))
        await self.add_cog(Scraper(self))
