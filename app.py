import discord
import os
import logging, logging.handlers
from bot import Bot
from dotenv import load_dotenv
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

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)
logging.getLogger('discord.gateway').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='/var/logs/lblcs/lblcs.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = Bot(guild_id, intents, supabase_client)



client.run(discord_token, log_handler=None, )
