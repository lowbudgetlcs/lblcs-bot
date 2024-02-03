import discord
from discord.ext import commands
import os
import user
from dotenv import load_dotenv
import logging

load_dotenv('../.env')
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix='', intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} ID {self.application_id}')
        users = []
        members = self.get_guild(GUILD_ID).members
        for member in members:
            users.append(user.User(member.id, member.name, member.display_name))
        print(users)

    async def setup_hook(self):
        print('Loading extensions...')
        await self.load_extension('tournaments')
        await self.tree.sync(guild=self.get_guild(GUILD_ID))


client = Client()

client.run(TOKEN, log_level=logging.DEBUG)
