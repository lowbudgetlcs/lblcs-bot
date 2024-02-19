import discord
import os
import logging.handlers
from src.bot import Bot
from dotenv import load_dotenv
from src.db.database import Supabase

# Set up environmental variables
load_dotenv('.env')
discord_token = os.getenv('DISCORD_TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
provider_id = int(os.getenv("PROVIDER_ID"))
tournament_id = int(os.getenv("TOURNAMENT_ID"))
tournament_code_endpoint = os.getenv("TOURNAMENT_CODE_ENDPOINT")

# Supabase setup
db_client: Supabase = Supabase(supabase_url, supabase_key)

# Bot setup
intents = discord.Intents.default()

# Logging setup
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
# logging.getLogger('discord.http').setLevel(logging.INFO)
# logging.getLogger('discord.gateway').setLevel(logging.INFO)

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

# Client instantiation + run
client = Bot(guild_id, intents, db_client)
client.run(discord_token, log_handler=None, )
