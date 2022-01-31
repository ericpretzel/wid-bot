import asyncio
import config
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from util.wordle_game import InvalidGuessException, WordleGame

class Wordle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.running_games = dict()

    @slash_command(
        guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description="Play a game of Wordle."
    )
    async def wordle(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        # check if you are already in game
        if ctx.author in self.running_games:
            return await ctx.respond('You are already playing a game!', ephemeral=True)

        game = WordleGame()
        self.running_games[ctx.author] = game
        
        await ctx.respond("Game started. Guess a five letter word.")

        embed = discord.Embed(title='Wordle Game')
        
        """
        Checks messages sent for when the user sends a word for wordle.
        Also checks for a signal message when a member sends the "quit" command.
        When this check returns true, the loop below will proceed past the first await.
        """
        def check(id):
            def inner_check(msg: discord.Message):
                if msg.author == self.bot.user:
                    return msg.content == self.quit_message(id)
                return msg.author == ctx.author and msg.channel == ctx.channel
            return inner_check

        while game.result is None:
            try:
                msg = await self.bot.wait_for('message', check=check(ctx.author.id), timeout=180.0)
                await msg.delete()
                if msg.author == self.bot.user:
                    # signalled to quit, so make sure it doesn't perform any more game logic
                    break

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

        del self.running_games[ctx.author]

        if game.result is True:
            embed.set_footer(text='You won!')
        elif game.result is False:
            embed.set_footer(text='You lost! Correct answer: ' + game.word)
        elif game.result is None:
            embed.set_footer(text='You took too long to respond! Correct answer: ' + game.word)
        return await ctx.edit(embed=embed)

    @wordle.error
    async def wordle_error(self, ctx, error):
        return await ctx.respond(error) 

    """
    Sends a message that the check will pick up to stop the game
    """
    @slash_command(
        guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description='Quit your current Wordle game.'
    )
    async def quit(self, ctx: discord.ApplicationContext):
        try:
            game = self.running_games[ctx.author]
            game.result = False
            await ctx.interaction.channel.send(self.quit_message(ctx.author.id))
            return await ctx.respond('Successfully quit your game.', ephemeral=True)
        except KeyError:
            return await ctx.respond('You are not in a game!', ephemeral=True)
    
    def quit_message(self, id):
        return 'Stopping game: ' + str(id)
       
def setup(bot):
    bot.add_cog(Wordle(bot))