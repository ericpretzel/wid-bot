import json
import config
import discord
from util.emojifier import Emojifier
from discord.ext import commands
from discord.commands import slash_command, message_command

class Fun(commands.Cog):
    def __init__(self, bot, emojifier):
        self.bot = bot
        self.emojifier = emojifier
    
    @message_command(name='Emojify', guild_ids=[config.GUILD_ID])
    async def emojify(self, ctx: discord.ApplicationContext, msg: discord.Message):
        emojified = self.emojifier.emojify(msg.content)
        if len(emojified) > 2000:
            await ctx.interaction.response.send_message(content='That message is too long to be emojified!', ephemeral=True)
        else:
            await ctx.interaction.response.send_message(content=emojified)

    @message_command(name='Ratio', guild_ids=[config.GUILD_ID])
    async def ratio(self, ctx: discord.ApplicationContext, msg: discord.Message):
        emojis = ['🇷', '🇦', '🇹', '🇮', '🇴']
        if any(emoji in emojis for emoji in msg.reactions):
            await ctx.interaction.response.send_message('Cannot ratio. Already has reactions.', ephemeral=True)
        else:
            for emoji in emojis:
                await msg.add_reaction(emoji=emoji)
            await msg.add_reaction(emoji='😂')
            await ctx.interaction.response.send_message('Done', ephemeral=True)

def setup(bot):
    # load emojis from file
    with open(config.EMOJI_MAPPINGS) as f:
        mappings = json.load(f)
        emojifier = Emojifier(mappings)

    bot.add_cog(Fun(bot, emojifier))
