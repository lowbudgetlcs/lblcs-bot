import discord
from discord import SelectOption
import cachetools.func

# TODO: Investiage if caching is actually helpful

@cachetools.func.ttl_cache(maxsize=10, ttl=3600)
def fetch_leagues() -> list[SelectOption]:
    # TODO: Fetch tournament list from supabase
    return [
        SelectOption(label="Economy", value="ECONOMY"),
        SelectOption(label="Commercial", value="COMMERCIAL"),
        SelectOption(label="Financial", value="FINANCIAL"),
        SelectOption(label="Executive", value="EXECUTIVE")
        ]

@cachetools.func.ttl_cache(maxsize=10, ttl=600)
def fetch_teams() -> list[SelectOption]:
    # TODO: Fetch team list of ALL TEAMS
    return [SelectOption(label="Team 1", value="1"), SelectOption(label="Team 2", value="2")]


class GameCreationModal(discord.ui.Modal, title='GameCreation'):
    # TODO: ENABLE AUTOCOMPLETE ON TEAM SELECTIONS!
    league = discord.ui.Select(
        placeholder='Select a league!',
        row=0,
        options=fetch_leagues(),
    )

    team1 = discord.ui.Select(
        placeholder='First team...',
        row=2,
        options=fetch_teams()
    )

    team2 = discord.ui.Select(
        placeholder='Second team...',
        row=2,
        options=list()
    )

    async def on_submit(self, interaction: discord.Interaction):
        code = 0
        await interaction.response.send_message(f'League: {self.league}\n{self.team1} v.s. {self.team2}\nCode:: {code}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
