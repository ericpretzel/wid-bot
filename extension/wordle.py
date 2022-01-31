import asyncio
import config
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from util.wordle_game import InvalidGuessException, WordleGame


class Wordle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.running_games = []

    @slash_command(
        guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description="Play a game of Wordle."
    )
    async def wordle(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        # check if you are already in game
        if any(game.player == ctx.author for game in self.running_games):
            return await ctx.respond('You are already playing a game!', ephemeral=True)

        game = WordleGame(ctx.author)
        self.running_games.append(game)
        
        await ctx.respond("Game started. Guess a five letter word.")

        embed = discord.Embed(title='Wordle Game')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        while game.result() is None:
            try: 
                msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                await msg.delete()
                guess = msg.content.lower().strip()

                ans = ' '.join(game.check(guess))
                guess = ' '.join([f':regional_indicator_{c}:' for c in guess])
                embed.add_field(name=guess, value=ans, inline=False)
                await ctx.edit(embed=embed)
            except asyncio.TimeoutError:
                break
            except InvalidGuessException as e:
                await ctx.respond(e.args[0], ephemeral=True)
                continue

        self.running_games.remove(game)

        if game.result() is True:
            embed.set_footer(text='You won!')
        elif game.result() is False:
            embed.set_footer(text='You lost! Correct answer: ' + game.word)
        elif game.result() is None:
            embed.set_footer(text='You took too long to respond! Correct answer: ' + game.word)
        return await ctx.edit(embed=embed)

    @wordle.error
    async def wordle_error(self, ctx, error):
        return await ctx.respond(error) 

def setup(bot):
    bot.add_cog(Wordle(bot))