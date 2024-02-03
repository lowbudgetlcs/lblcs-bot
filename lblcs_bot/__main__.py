import discord
import os
from bot import Bot
from dotenv import load_dotenv
import logging

#Set up environmental variables
load_dotenv('.env')
token = os.getenv('TOKEN')
guild_id = os.getenv('GUILD_ID')


#Bot setup
intents = discord.Intents.default()
client = Bot(guild_id, intents)

#Logging Setup

client.run(token, log_level=logging.INFO, root_logger=True)