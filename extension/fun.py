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

def setup(bot):
    # load emojis from file
    with open(config.EMOJI_MAPPINGS) as f:
        mappings = json.load(f)
        emojifier = Emojifier(mappings)

    bot.add_cog(Fun(bot, emojifier))
