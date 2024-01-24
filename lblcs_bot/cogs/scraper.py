from discord.ext import commands

class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @command.command()
    async def test_command(self,ctx):
        pass