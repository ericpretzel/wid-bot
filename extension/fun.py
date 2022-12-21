import json
import config
import discord
from util.emojifier import Emojifier
from discord.ext import commands
from discord.commands import slash_command, message_command, user_command
from discord.utils import escape_mentions
import aiosqlite
import markovify
import random

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
        await ctx.defer()
        emojis = ['🇷', '🇦', '🇹', '🇮', '🇴']
        if any(emoji in emojis for emoji in msg.reactions):
            await ctx.interaction.response.send_message('Cannot ratio. Already has reactions.', ephemeral=True)
        else:
            for emoji in emojis:
                await msg.add_reaction(emoji=emoji)
            await msg.add_reaction(emoji='😂')
            await ctx.respond('Done', ephemeral=True)

    @user_command(name="Unleash Demons", description='Unleash their inner demons.')
    async def demons(self, ctx: discord.ApplicationContext, mem: discord.Member):
        await ctx.defer()
        async with aiosqlite.connect(config.DB_FILE) as con:
            try:
                messages = await con.execute_fetchall("""SELECT content FROM messages WHERE author_id=(?)""", (mem.id,))
                messages = [msg[0] for msg in messages] # unwrap it bc they are returned as tuples
            except:
                await ctx.respond('Could not summon demons, likely because the messages table does not exist (yet). Trying again later.')
                return

        # messages must meet these criteria to be considered for the markov chain corpus:
        msg_filters = [
            lambda m: len(m) >= 6, # no super short one-word messages
            lambda m: not m.startswith('http'), # no standalone links
            lambda m: not (m.startswith(':') and m.find(':', 1) == len(m)-1) # no standalone emojis
        ]
        num_sentences = 15

        corpus = [msg.replace('.', '\n') for msg in messages if all(msg_filter(msg) for msg_filter in msg_filters)]
        model = markovify.NewlineText(input_text='\n'.join(corpus), well_formed=False)
        
        message = f"**{mem.display_name}'s demons:**\n"
        message += '. '.join(filter(None, ([model.make_sentence(min_words=random.randint(2, 10)) for _ in range(num_sentences)])))
        message = escape_mentions(message)
        if len(message) > 2000:
            message = message[:2000-3] + '...'
        return await ctx.respond(message)

    @slash_command(guild_ids=[config.GUILD_ID], 
        description='Holy fax')
    async def hf(self, ctx: discord.ApplicationContext):
        return await ctx.respond('Holy fax')

def setup(bot):
    # load emojis from file
    with open(config.EMOJI_MAPPINGS) as f:
        mappings = json.load(f)
        emojifier = Emojifier(mappings)

    bot.add_cog(Fun(bot, emojifier))
