from discord.ext import commands, tasks
import lblcs_bot.models
from lblcs_bot.cogs.scraper import Scraper


class Bot(commands.Bot):
    def __init__(self,guild_id,intents):
        super().__init__('!',intents=intents)
        self.guild_id = guild_id

    async def on_ready(self):

        # print(f'{self.guild_id}')
        # guild = self.get_guild(self.guild_id)
        # print(f'{guild}')
        # members = guild.members
        # for member in members:
        #     print(f'{member.roles}')
        await self.add_cog(Scraper(self))
        print('Success')