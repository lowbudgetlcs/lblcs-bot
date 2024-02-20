import discord
import logging
import os
import requests
from src.models.metadata import Metadata


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


class CodeGenerationModal(discord.ui.Modal, title='CodeGenerationModal'):
    def __init__(self, bot_i):
        super().__init__()
        self.bot = bot_i

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
        # ------- VALIDATE FORM -------
        leagues = await self.bot.supabase.fetch_divisions()
        logging.info(f'League Input:{self.league.value}')
        logging.info(f'Leagues: {leagues}')
        if self.league.value.upper() not in [league["division_name"] for league in leagues]:
            raise Exception(f'{self.league.value} not found! Please check for typos and try again.')
        league_name = self.league.value.upper()
        league_id = [league["division_id"] for league in leagues if league["division_name"] == league_name][0]
        print(f"League ID: {league_id}")

        team1 = self.team1.value
        team1_id = await self.bot.supabase.fetch_like_team(team1)
        team2 = self.team2.value
        team2_id = await self.bot.supabase.fetch_like_team(team2)

        if team1_id == team2_id:
            raise Exception("Teams cannot play themselves! Try again!")

        team_id_lst = [team1_id, team2_id]

        try:
            game = int(self.game.value)
        except ValueError:
            raise Exception("Game must be an integer! i.e 1 for game 1, 2 for game 2 etc...")

        # ------- FETCH OR GENERATE SERIES ID -------
        series_id = await self.bot.supabase.fetch_series_id(team_id_lst)

        # ------- GENERATE TCODE WITH METADATA -------
        metadata: Metadata = Metadata(series_id=series_id, league=league_id,
                                      teams=team_id_lst, game=game)
        code = await generate_code(metadata)

        # ------- WRITE CODE TO SERVER -------
        league = await self.bot.supabase.fetch_division_by_id(league_id)
        team1 = await self.bot.supabase.fetch_team_by_id(team1_id)
        team2 = await self.bot.supabase.fetch_team_by_id(team2_id)

        await interaction.response.send_message(
            f'## {league}\n__**{team1}**__ v.s. __**{team2}**__\nCode:: `{code}`', ephemeral=False)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logging.warning(error)
        await interaction.response.send_message(
            f'Oops, we ran into an error!\nHere is the error:: {error}\nVery likely, this is the result of a typo. If the printed error message is confusing or you are positive there is no typo, please open an urgent ticket immediately!',
            ephemeral=True)
