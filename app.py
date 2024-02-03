import discord
import os
from bot import Bot
from dotenv import load_dotenv
import logging
from supabase import create_client, Client

#Set up environmental variables
load_dotenv('.env')
discord_token = os.getenv('DISCORD_TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
provider_id = int(os.getenv("PROVIDER_ID"))
tournament_id = int(os.getenv("TOURNAMENT_ID"))
tournament_code_endpoint = os.getenv("TOURNAMENT_CODE_ENDPOINT")


#Supabase setup
supabase_client:Client = create_client(supabase_url, supabase_key)

#Bot setup
intents = discord.Intents.default()
client = Bot(guild_id, intents, supabase_client)

client.run(discord_token, log_level=logging.INFO, root_logger=True)
