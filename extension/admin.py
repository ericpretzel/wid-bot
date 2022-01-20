import config
import discord
from discord.commands import slash_command
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # deletes messages if they are sent by blacklisted user in the given channel
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.id in config.blacklist.values() and msg.channel.id == config.PRIVATE_PORN_CHANNEL_ID:
            await msg.delete()

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID])
    async def shart(self, ctx: discord.ApplicationContext):
        return await ctx.respond('poo')


def setup(bot):
    bot.add_cog(Admin(bot))