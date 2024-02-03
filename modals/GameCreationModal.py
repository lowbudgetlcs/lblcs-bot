import discord
import logging
import os
import requests
from supabase import Client
from models.metadata import Metadata
import json

async def generate_code(metadata: Metadata) -> str | None:
    logging.info("Generating code")
    tournament_code_endpoint = os.getenv("TOURNAMENT_CODE_ENDPOINT")
    tournament_id = os.getenv("TOURNAMENT_ID")
    riot_token = os.getenv("RIOT_TOKEN")
    url = f"{tournament_code_endpoint}{tournament_id}"
    headers = {
        "X-Riot-Token": riot_token
    }
    body = {
        "mapType": "SUMMONERS_RIFT",
        "metadata": metadata.serialize(),
        "pickType": "TOURNAMENT_DRAFT",
        "spectatorType": "ALL",
        "teamSize": 5
    }
    code_response = requests.post(url, headers=headers, json=body)
    if code_response.status_code != 200:
        logging.error(code_response)
        raise Exception("Riot API Error! Contact ruuffian or open urgent ticket immediately!")
    return code_response.json()[0]


async def fetch_leagues() -> list[str]:
    logging.info("Fetching leagues")
    return ["Economy", "Commercial", "Financial", "Executive"]


async def fetch_teams(supabase: Client) -> list[str]:
    logging.info("Fetching teams")
    data = supabase.table("teams").select("team_name").execute()
    teams = data.model_dump()
    valid_teams = [team["team_name"] for team in teams["data"]]
    return valid_teams

class GameCreationModal(discord.ui.Modal, title='GameCreation'):
    def __init__(self, supabase: Client):
        super().__init__()
        self.supabase = supabase

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

        leagues = await fetch_leagues()
        teams = await fetch_teams(self.supabase)

        metadata: Metadata = Metadata(league=self.league.value, team1=self.team1.value, team2=self.team2.value)

        # TODO: Check that the league and both teams EXIST and ARE LEGAL OPPONENTS
        #   1. TEAMS ARE IN THE SAME LEAGUE
        if metadata.league not in leagues:
            raise Exception("Not valid League!")
        elif metadata.team1 not in teams:
            raise Exception("Team 1 invalid!")
        elif metadata.team2 not in teams:
            raise Exception("Team 2 invalid!")
        elif metadata.team1.lower() == metadata.team2.lower():
            raise Exception("Teams cannot play themselves!")
        try:
            metadata.game = int(self.game.value)
        except ValueError:
            raise Exception("Game must be an integer!")

        code = await generate_code(metadata)

        await interaction.response.send_message(f'## {self.league}\n__**{self.team1}**__ v.s. __**{self.team2}**__\nCode:: `{code}`', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logging.warning(error)
        await interaction.response.send_message(f'Here is the error:: {error}\nIt\'s probably just a typo- if so, resubmit with corrections. If the aforementioned error is weird or confusing, please open an urgent ticket immediately!', ephemeral=True)
