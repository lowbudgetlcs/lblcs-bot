import discord
import os
import user
import csv
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    users = []
    members = client.guilds[0].members
    for member in members:
        users.append(user.User(member.id,member.name,member.display_name))
        

client.run(TOKEN)