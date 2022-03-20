import config
import discord
from discord.commands import slash_command
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.GUILD_ID])
    async def shart(self, ctx: discord.ApplicationContext):
       return await ctx.respond('poo')

def setup(bot):
    bot.add_cog(Admin(bot))