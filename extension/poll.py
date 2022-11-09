from datetime import timedelta
import config
import discord
from discord.ext import commands
from discord.commands import slash_command, message_command, Option
from discord.utils import utcnow, format_dt

class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        guild_ids=[config.GUILD_ID],
        description='Create a poll for people to vote on.'
    )
    async def poll(self, ctx: discord.ApplicationContext,
        num_options: Option(
            int,
            "Number of selectable options",
            name='options',
            min_value=2, max_value=4
        ),
        view_timeout: Option(
            float,
            "Length (in minutes) the poll should last",
            name='minutes',
            min_value=1, max_value=24*60, default=60
        ),
        anonymous: Option(
            str,
            "Whether or not to hide people's votes",
            choices=['true', 'false'],
            default='false'
        )):
        # convert view_timeout from minutes to seconds
        modal = PollModal(num_options, view_timeout * 60, anonymous)
        #modal = PollModal(num_options, 10)
        await ctx.send_modal(modal)

class PollModal(discord.ui.Modal):
    """
    Represents a modal dialogue for a user to create a poll.
    The poll is then displayed to the channel in a PollView.
    """
    def __init__(self, num_options, view_timeout, anonymous):
        super().__init__(title='Create Poll')
        self.view_timeout = view_timeout
        self.anonymous = anonymous

        topic = discord.ui.InputText(style=discord.InputTextStyle.short, placeholder='Topic', label='Topic')
        self.add_item(topic)
        for i in range(num_options):
            label = f'Option #{i+1}'
            item = discord.ui.InputText(
                style=discord.InputTextStyle.short,
                placeholder="Option",
                label=label,
                max_length=25
            )
            self.add_item(item)

    async def callback(self, ctx: discord.Interaction):
        """
        Creates and sends a PollView based on what was input in the modal. 
        """
        topic = self.children[0].value
        options = [c.value for c in self.children[1:]]
        view = PollView(topic, options, self.view_timeout, self.anonymous)
        await ctx.response.send_message('Poll created.', ephemeral=True)
        msg = await ctx.channel.send(view=view, embed=view.embed)
        view.message = msg

class PollButton(discord.ui.Button):
    """
    Button that represents a choice in the poll.
    Updates the PollView via `update_votes()`.
    """
    async def callback(self, ctx: discord.Interaction):
        await ctx.response.defer()
        view: PollView = self.view
        # manually check if the time is up and poll should be done
        # because on_timeout is incredibly unreliable for some reason :)
        if utcnow() > view.expiration:
            await view.end_poll()
        else: 
            await view.update_votes(ctx, self.custom_id)

class PollView(discord.ui.View):
    """
    Represents a poll. Contains PollButtons that the users press to cast their vote.
    Keeps track of votes and updates when users vote.
    """
    def __init__(self, topic, options, timeout, anonymous):
        super().__init__(timeout=timeout)
        self.message: discord.InteractionMessage = None # this value will be updated immediately in PollModal callback
        self.votes = dict()
        self.anonymous = anonymous

        now = utcnow()
        self.expiration = now + timedelta(seconds=timeout) 
        self.embed = discord.Embed(
            title=("" if anonymous == 'false' else "Anonymous ") + f"Poll (until {format_dt(self.expiration)})",
            description=f'**{topic}**',
            color=discord.Color.random()
        )

        for i, opt in enumerate(options):
            button = PollButton(label=opt, custom_id=f'{int(now.timestamp())}_poll_opt_{i}', style=discord.ButtonStyle.blurple)
            self.add_item(button)
            self.votes[button.custom_id] = list()
        
        self.update_embed()
    
    async def update_votes(self, ctx: discord.Interaction, id: str):
        """
        Called when a user votes for an option by pressing a PollButton attached to this view.
        """
        # check whether the user is adding, changing, or cancelling their vote
        cancelling = False
        for option_id, users in self.votes.items():
            if ctx.user.name in users:
                users.remove(ctx.user.name)
                cancelling = option_id == id
                break
        if not cancelling:
            # user is adding or changing their vote
            users = self.votes[id]
            users.append(ctx.user.name)
        
        self.update_embed()

        await self.message.edit(view=self, embed=self.embed)
    
    def update_embed(self):
        """
        Updates the embed attached to this view.
        """
        self.embed.clear_fields()

        total_votes = sum(map(len, self.votes.values())) or 1 # avoid div by 0

        option: PollButton # for type hinting
        for option in self.children:
            u = self.votes[option.custom_id]
            # show only first 10 users
            users = ', '.join(u[:10]) if len(u) > 0 else 'No votes'
            if (self.anonymous == 'true'):
                users = ''
            percent = len(u) / total_votes
            bar = ('█' * round(percent*20) ).ljust(20, '░')
            
            self.embed.add_field(
                name=f'{option.label} - {len(u)}',
                value=f'{bar} - {round(percent*100)}%\n{users}',
                inline=False
            )
    
    async def end_poll(self):
        # disable buttons
        button:PollButton
        for button in self.children:
            button.disabled = True
        # find winner(s)
        maxlen = max(map(len, self.votes.values()))
        winners = [i for i, opt in enumerate(self.votes) if len(self.votes[opt]) == maxlen and maxlen > 0]
        # display winner(s)
        self.embed.set_footer(text='Poll Result: ' + (', '.join([self.children[i].label for i in winners]) if maxlen > 0 else 'None'))
        self.stop() # the view will now stop listening to interactions/new votes
        await self.message.edit(view=self, embed=self.embed)

    async def on_timeout(self) -> None:
        await self.end_poll()
        
def setup(bot):
    bot.add_cog(Poll(bot))
