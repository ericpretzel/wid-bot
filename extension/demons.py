import config
import discord
from discord.ext import commands
from discord.commands import user_command, slash_command, permissions
from discord.utils import escape_mentions
import util.demon_manager as dm

class Demons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @user_command(name="Unleash Demons", guild_ids=[config.GUILD_ID])
    async def demons(self, ctx: discord.ApplicationContext, mem: discord.Member):
        message = f"**{mem.display_name}'s demons:**\n"
        try:
            message += dm.generate_sentences(ctx.guild_id, mem.id, 15)
        except dm.ModelNotFoundException:
            return await ctx.respond('These demons have not been summoned yet...', ephemeral=True)
        message = escape_mentions(message)
        if len(message) > 2000:
            message = message[:2000-3] + '...'
        await ctx.respond(message)

    @slash_command(
        description="Begin the ritual.",
        guild_ids=[config.GUILD_ID]
    )
    @commands.is_owner()
    async def summon_demons(self, ctx: discord.ApplicationContext):
        """
        Fetches every single message from the server.
        EXTREMELY TIME CONSUMING.
        """

        await ctx.respond("The ritual has begun.", ephemeral=True)
        messages_parsed = 0
        guild = ctx.guild
        print(f'Gathering data from guild {guild.id}...')
        data = dict()
        for channel in guild.text_channels:
            async for message in channel.history(limit = None) \
                .filter(lambda msg: len(msg.content) > 6) \
                .filter(lambda msg: not msg.content.startswith('http')) \
                .filter(lambda msg: not msg.content.startswith(':')):
                user_id = message.author.id
                if user_id not in data:
                    data[user_id] = list()
                data[user_id].append(message.content)
                messages_parsed += 1
                if messages_parsed % 100 == 0:
                    print(f'messages_parsed: {messages_parsed}')
                    print(f'current message: {message.content}')
        print('Done gathering. Generating report.')
        dm.generate_demon_report(guild.id, data)
        print('Report generated!')


def setup(bot):
    bot.add_cog(Demons(bot))