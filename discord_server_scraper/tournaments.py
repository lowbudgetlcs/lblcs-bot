import cachetools.func
import discord, discord.ext.commands as commands
from discord import app_commands, SelectOption

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

def check_code_role(interaction: discord.Interaction) -> bool:
    accepted_roles = ["Captain", "Admin", "Sub-Team-Lead", "Dev"]
    return True in [(x in accepted_roles) for x in interaction.user.roles]

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tournaments = []

    @app_commands.command(name='tcode')
    @app_commands.check(check_code_role)
    async def tcode(self, ctx):
        # TODO: Hit RIOT API endpoint to generate tcode
        await ctx.send("Hello world!")


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

async def setup(bot):
    await bot.add_cog(Tournament(bot))

