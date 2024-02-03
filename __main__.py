import discord
import os
from lblcs_bot.bot import Bot
from dotenv import load_dotenv
import logging

#Set up environmental variables
load_dotenv('lblcs_bot/.env')
token = os.getenv('TOKEN')
guild_id = os.getenv('GUILD_ID')


#Bot setup
intents = discord.Intents.default()
client = Bot(guild_id, intents)

client.run(token, log_level=logging.INFO, root_logger=True)