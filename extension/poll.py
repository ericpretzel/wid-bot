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
            "Length (in hours) the poll should last",
            name='hours',
            min_value=0.25, max_value=24.0, default=12.0
        )):
        # convert view_timeout from hours to seconds
        modal = PollModal(num_options, view_timeout * 60 * 60)
        await ctx.interaction.response.send_modal(modal)
    
    @message_command(
        name='End Poll',
        guild_ids=[config.GUILD_ID]
    )
    async def end_poll(self, ctx: discord.ApplicationContext, msg: discord.Message):
        """
        End the poll early
        """
        view = discord.ui.View.from_message(msg)
        # TODO do stuff
        await ctx.respond('Done', ephemeral=True)

class PollModal(discord.ui.Modal):
    """
    Represents a modal dialogue for a user to create a poll.
    The poll is then displayed to the channel in a PollView.
    """
    def __init__(self, num_options, view_timeout):
        super().__init__('Create Poll')
        self.view_timeout = view_timeout

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
        view = PollView(topic, options, self.view_timeout)
        await ctx.response.send_message(view=view, embed=view.embed)
        view.message = await ctx.original_message()

class PollButton(discord.ui.Button):
    """
    Button that represents a choice in the poll.
    Updates the PollView via `update_votes()`.
    """
    async def callback(self, ctx: discord.Interaction):
        await ctx.response.defer()
        view: PollView = self.view
        await view.update_votes(ctx, self.custom_id)

class PollView(discord.ui.View):
    """
    Represents a poll. Contains PollButtons that the users press to cast their vote.
    Keeps track of votes and updates when users vote.
    """
    def __init__(self, topic, options, timeout):
        super().__init__(timeout=timeout)
        self.message: discord.InteractionMessage = None # this value will be updated immediately in PollModal callback
        self.votes = dict()

        now = utcnow()
        expiration = now + timedelta(seconds=timeout) 
        self.embed = discord.Embed(
            title=f"Poll (until {format_dt(expiration)})",
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
            u = self.votes[option.custom_id][:10]
            users = ', '.join(u) if len(u) > 0 else 'No votes'
            percent = len(u) / total_votes
            bar = ('█' * round(percent*20) ).ljust(20, '░')
            
            self.embed.add_field(
                name=f'{option.label} - {len(u)}',
                value=f'{bar} - {round(percent*100)}%\n{users}',
                inline=False
            )
    
    async def on_timeout(self):
        """
        Edits the message to show the winning choice(s).
        """
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
        
def setup(bot):
    bot.add_cog(Poll(bot))
