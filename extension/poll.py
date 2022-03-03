import config
import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(
        guild_ids=[config.GUILD_ID],
        description='Create a poll for people to vote on.'
    )
    async def poll(self, ctx: discord.ApplicationContext,
        options: Option(
            int,
            "Number of selectable options",
            min_value=2, max_value=4
        )):
        modal = PollModal(options)
        await ctx.interaction.response.send_modal(modal)

class PollModal(discord.ui.Modal):
    """
    Represents a modal dialogue for a user to create a poll.
    The poll is then displayed to the channel in a PollView.
    """
    def __init__(self, options):
        super().__init__('Create Poll')

        topic = discord.ui.InputText(style=discord.InputTextStyle.paragraph, placeholder="Topic", label="Topic")
        self.add_item(topic)

        for i in range(options):
            label = f'Option #{i+1}'
            item = discord.ui.InputText(style=discord.InputTextStyle.short, placeholder="Option", label=label, max_length=50)
            self.add_item(item)

    async def callback(self, ctx: discord.Interaction):
        """
        Creates and sends a PollView to the channel based on what was input in the modal. 
        """
        description = self.children[0].value
        options = [c.value for c in self.children[1:]]
        view = PollView(description, options)
        await ctx.response.send_message(view=view, embed=view.generate_embed())

class PollButton(discord.ui.Button):
    async def callback(self, ctx: discord.Interaction):
        view: PollView = self.view
        await view.update_votes(ctx, self.label)

class PollView(discord.ui.View):
    def __init__(self, description, options):
        super().__init__()
        self.description = description
        self.votes = dict()

        for opt in options: 
            button = PollButton(label=opt)
            self.add_item(button)
            self.votes[opt] = list()
    
    async def update_votes(self, ctx: discord.Interaction, option: str):
        """
        Called when a user votes by pressing a PollButton attached to this view.
        """
        # check if the user is changing their vote
        for users in self.votes.values():
            if ctx.user.display_name in users:
                users.remove(ctx.user.display_name)
                break
        users = self.votes[option]
        users.append(ctx.user.display_name)
        await ctx.response.edit_message(view=self, embed=self.generate_embed())
    
    def generate_embed(self) -> discord.Embed:
        """
        Generate an embed showing the (ongoing) results of the poll.

        It would be ideal to edit an existing embed object instead of creating a new one every time but that's too tedious lol
        """
        embed = discord.Embed(title=self.description)
        option: PollButton # for type hinting
        for option in self.children:
            users = self.votes[option.label]
            embed.add_field(name=option.label, value=', '.join(users) if len(users) > 0 else 'Nobody', inline=False)
        return embed
        
def setup(bot):
    bot.add_cog(Poll(bot))
