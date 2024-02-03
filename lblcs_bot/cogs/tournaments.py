import discord, discord.ext.commands as commands
from discord import app_commands
import logging
import cachetools.func
import json

def check_code_role(interaction: discord.Interaction) -> bool:
    accepted_roles = ["Captain", "Admin", "Sub-Team-Lead", "Dev"]
    authorized = [(x.name in accepted_roles) for x in interaction.user.roles]
    return True in authorized

async def fetch_leagues() -> list[str]:
    logging.info("Fetching leagues")
    return ["Economy", "Commercial", "Financial", "Executive"]

@cachetools.func.ttl_cache(maxsize=10, ttl=600)
async def fetch_teams() -> list[str]:
    logging.info("Fetching teams")
    # TODO: Fetch team list of ALL TEAMS from supabase
    return ["Team 1", "Team 2"]

async def generate_code(metadata) -> str:
    logging.info("Generating code")
    # TODO: Generate tournament code through Riot api
    return json.dumps(metadata)

class Tournament(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading Tournament cog")
        self.bot = bot
        self.tournaments = []

    @app_commands.command(name='generate-tournament-code', description="Used to generate a tournament code!")
    @app_commands.check(check_code_role)
    async def tcode(self, interaction: discord.Interaction):
        # TODO: Hit RIOT API endpoint to generate tcode
        await interaction.response.send_modal(GameCreationModal())


class GameCreationModal(discord.ui.Modal, title='GameCreation'):
    # TODO: ENABLE AUTOCOMPLETE ON TEAM SELECTIONS!
    league = discord.ui.TextInput(
        label='League',
        placeholder='Economy, Commercial...',
        required=True,
    )

    team1 = discord.ui.TextInput(
        label='Team 1',
        placeholder='First team',
        required=True
    )

    team2 = discord.ui.TextInput(
        label='Team 2',
        placeholder='Second team',
        required=True
    )

    game = discord.ui.TextInput(
        label='Game #',
        placeholder='1,2,3...',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        logging.info("Code generation started")
        leagues = await fetch_leagues()
        teams = await fetch_teams()

        metadata = {'league': self.league.value, 'team1': self.team1.value, 'team2': self.team2.value}

        # TODO: Check that the league and both teams EXIST and ARE LEGAL OPPONENTS
        #   1. TEAMS ARE IN THE SAME LEAGUE
        if metadata["league"] not in leagues:
            raise Exception("Not valid League!")
        elif metadata["team1"] not in teams:
            raise Exception("Team 1 invalid!")
        elif metadata["team2"] not in teams:
            raise Exception("Team 2 invalid!")
        elif metadata["team1"].lower() == metadata["team2"].lower():
            raise Exception("Teams cannot play themselves!")
        try:
            metadata["game"] = int(self.game.value)
        except ValueError:
            raise Exception("Game must be an integer!")

        code = await generate_code(metadata)

        await interaction.response.send_message(f'## {self.league}\n__**{self.team1}**__ v.s. __**{self.team2}**__\nCode:: `{code}`', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logging.warning(error)
        await interaction.response.send_message(f'Here is the error:: {error}\nIt\'s probably just a typo- if so, resubmit with corrections. If the aforementioned error is weird or confusing, please open an urgent ticket immediately!', ephemeral=True)
