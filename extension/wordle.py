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
    async def wordle(self, ctx: discord.ApplicationContext,
        difficulty: Option(
            str, 
            "In hard mode, you must use letters that were guessed correctly in subsequent guesses.",
            choices=['normal', 'hard'],
            default='normal'
        )):
        await ctx.defer()
        
        self.ensure_not_in_game(ctx)

        game = WordleGame(hard = difficulty=='hard' )
        self.running_games[ctx.author] = game
        
        embed = discord.Embed(title=f'Wordle Game ({difficulty.capitalize()})')
        keyboard = self.build_keyboard(game)

        await ctx.respond(embeds=[embed, keyboard])
        
        def check(id):
            """
            Checks messages sent for when the user sends a word for wordle.
            Also checks for a signal message when a member sends the "quit" command.
            When this check returns true, the loop below will proceed past the first await.
            """
            def inner_check(msg: discord.Message):
                if msg.author == self.bot.user:
                    return msg.content == self.quit_message(id)
                return msg.author == ctx.author and msg.channel == ctx.channel
            return inner_check

        while game.result is None: # 'None' means the game has not ended yet.
            try:
                msg = await self.bot.wait_for('message', check=check(ctx.author.id), timeout=300.0)
                await msg.delete()
                if msg.author == self.bot.user:
                    # signalled to quit, so make sure it doesn't perform any more game logic
                    break

                guess = msg.content.lower().strip()

                emojis = game.check(guess)
                
                keyboard = self.build_keyboard(game)

                # \u200c is zwsp aka invisible unicode character
                # used to make emojis not as big on mobile
                ans = '\u200c '.join(emojis)
                guess = '\u200c '.join([f':regional_indicator_{c}:' for c in guess])
                embed.add_field(name=guess, value=ans, inline=False)

                await ctx.edit(embeds=[embed, keyboard])
            except asyncio.TimeoutError:
                break # wait_for timed out, so quit the game.
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
        return await ctx.edit(embed=embed) # gets rid of the keyboard

    def build_keyboard(self, game: WordleGame) -> discord.Embed:
        """
        Returns an embed representing the keyboard from the user's game.
        """
        embed = discord.Embed(title='Keyboard')
        for s in ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']:
            name = '\u200c '.join([f':regional_indicator_{c}:' for c in s])
            value = '\u200c '.join([game.keyboard[c] for c in s])
            embed.add_field(name=name, value=value, inline=False)
        return embed

    @slash_command(
        guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description='Quit your current Wordle game.'
    )
    async def quit(self, ctx: discord.ApplicationContext):
        """
        Sends a message that the check in `wordle()` will pick up to stop the game.
        """
        game = self.ensure_in_game(ctx)
        game.result = False
        await ctx.interaction.channel.send(self.quit_message(ctx.author.id))
        return await ctx.respond('Successfully quit your game.', ephemeral=True)
    
    def ensure_in_game(self, ctx: discord.ApplicationContext) -> WordleGame:
        """
        Raises an exception if the player is not in a game.

        Handled in `cog_command_error()`.
        """
        try:
            game = self.running_games[ctx.author]
        except KeyError:
            raise Exception('You are not in a game!')
        return game

    def ensure_not_in_game(self, ctx: discord.ApplicationContext) -> None:
        """
        Raises an exception if the player is in a game.
        
        Handled in `cog_command_error()`.
        """
        if ctx.author in self.running_games:
            raise Exception('You are already in a game!')

    async def cog_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """
        Called whenever a command within this cog raises an error.
        """
        return await ctx.respond(error.args[0], ephemeral=True)

    def quit_message(self, id: int) -> str:
        """
        Message content indicating the player's game should be stopped.
        """
        return 'Stopping game: ' + str(id)
       
def setup(bot):
    bot.add_cog(Wordle(bot))
