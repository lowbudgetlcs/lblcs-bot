import discord
import os
from lblcs_bot.bot import Bot
from dotenv import load_dotenv
#Set up environmental variables
load_dotenv('.env')
token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD_ID'))

#Bot setup
intents = discord.Intents.all()
client = Bot(guild_id,intents)
client.run(token)