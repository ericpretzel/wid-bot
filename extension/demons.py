import config
import discord
from discord.ext import commands
from discord.commands import user_command
import markovify

class Demons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @user_command(name="Unleash Demons", guild_ids=[config.GUILD_ID])
    async def demons(self, ctx: discord.ApplicationContext, mem: discord.Member):
        await ctx.defer()
        messages = await self.gather_messages_from(mem)

        text = '\n'.join(messages)
        model = markovify.NewlineText(text, well_formed=False)
        
        sentences = '. '.join(model.make_short_sentence(max_chars=1750//15, test_output=False) for _ in range(15))
        print(sentences)
        await ctx.respond(f"{mem.display_name}'s demons: {sentences}")

    async def gather_messages_from(self, mem: discord.Member):
        messages = list()
        guild = mem.guild
        for channel in guild.text_channels:
            async for message in channel.history(limit=666) \
            .filter(lambda msg: msg.author == mem) \
            .filter(lambda msg: len(msg.content) > 10):
                messages.append(message.content)
        return messages




def setup(bot):
    bot.add_cog(Demons(bot))