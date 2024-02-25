import discord
from discord import app_commands
from discord.ext import commands
from src.models.user import User
import logging


class Scraper(commands.Cog):
    def __init__(self, bot):
        logging.info("Loading scraper cog")
        self.bot = bot

    def get_unsynced_users(self, teams, synced_users) -> [User]:
        discord_users = []
        assigned_team = 0
        guild = self.bot.get_guild(self.bot.guild_id)
        role = guild.get_role(585870102780575744)
        members = role.members
        for member in members:
            if member.id not in synced_users:
                roles = [role.name for role in member.roles]
                for team in teams:
                    if team["team_name"] in roles and member.name != "evdingus":
                        assigned_team = team["team_id"]
                        break
                if assigned_team != 0:
                    discord_users.append(User(member.id, member.name, member.display_name,assigned_team))
                    assigned_team = 0
        return discord_users

    async def get_teams(self) -> [str]:
        teams = await self.bot.supabase.fetch_all_teams()
        return teams

    async def get_synced_users(self):
        users = await self.bot.supabase.fetch_all_users()
        users = [user["user_id"] for user in users]
        return users
    @app_commands.command(name='sync-users', description="Used to sync users!")
    @app_commands.checks.has_role('Developer')
    async def sync_users(self, interaction: discord.Interaction):
        logging.info('Syncing users')
        teams = await self.get_teams()
        synced_users = await self.get_synced_users()
        users = self.get_unsynced_users(teams, synced_users)
        for user in users:
            logging.info(user)
            await self.bot.supabase.insert_user(user)