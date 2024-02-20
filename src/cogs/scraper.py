import discord
from discord import app_commands
from discord.ext import commands
from src.models.user import User
import logging


class Scraper(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading scraper cog")
        self.bot = bot

    def read_members(self, teams) -> [User]:
        discord_users = []
        guild = self.bot.get_guild(self.bot.guild_id)
        role = guild.get_role(585870102780575744)
        members = role.members
        for member in members:
            roles = [role.name for role in member.roles]
            for team in teams:
                if team.team_name in roles:
                    users.append(User(member.id, member.name, member.display_name, team.team_id))
        return users

    async def read_teams(self) -> [str]:
        teams = await self.bot.supabase.fetch_all_teams()

    @app_commands.command(name='sync-users', description="Used to sync users!")
    @app_commands.checks.has_role('Developer')
    async def sync_users(self, interaction: discord.Interaction):
        logging.info('Syncing users')
        teams = await self.read_teams()
        for team in teams:
            print(team)
        # users = self.read_members(teams)
        # for user in users:
        #     bot.supabase.insert_user(user)
