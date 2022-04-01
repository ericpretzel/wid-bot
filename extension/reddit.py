import config
import discord
from discord.ext import commands
from discord.ui import View
from discord import ButtonStyle
from util.reddit_scraper import get_subreddit_drama, get_aita

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reddit_group = discord.SlashCommandGroup('reddit', 'Commands which retrieve top posts from subreddits', guild_ids=[config.GUILD_ID])

    @reddit_group.command(description='What\'s trending on r/AmITheAsshole')
    async def aita(self, ctx: discord.ApplicationContext):
        try:
            await ctx.defer()
            post = await get_aita()
        except Exception as e:
            return await ctx.respond('Unable to find an asshole. Try the mirror.', ephemeral=True)  
        
        # must truncate embed descriptions to 4096 chars
        if len(post['desc']) > 4096:
            post['desc'] = post['desc'][:4096-3] + '...' 

        embed = discord.Embed(
            title=post['title'],
            url=f"https://reddit.com{post['link']}",
            description=post['desc']
        )
        embed.set_footer(text=f"{post['upvotes']} upvotes")
        embed.set_author(name=post['author'])

        await ctx.respond(embed=embed, view=AitaView(post))

    @reddit_group.command(description='What\'s trending on r/SubredditDrama')
    async def subreddit_drama(self, ctx: discord.ApplicationContext):
        try:
            await ctx.defer()
            post = await get_subreddit_drama()
        except Exception as e:
            return await ctx.respond('Unable to find a spicy story :/', ephemeral=True)  
        
        # must truncate embed descriptions to 4096 chars
        if len(post['desc']) > 4096:
            post['desc'] = post['desc'][:4096-3] + '...' 

        embed = discord.Embed(
            title=post['title'],
            url=f"https://reddit.com{post['link']}",
            description=post['desc']
        )
        embed.set_footer(text=f"{post['upvotes']} upvotes")
        embed.set_author(name=post['author'])

        await ctx.respond(embed=embed)

class AitaView(View):
    def __init__(self, post):
        super().__init__()
        self.post = post

    @discord.ui.button(label='YTA', style=ButtonStyle.red)
    async def yta_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response(button.label), ephemeral=True)

    @discord.ui.button(label='NTA', style=ButtonStyle.green)
    async def nta_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response(button.label), ephemeral=True)

    @discord.ui.button(label='ESH', style=ButtonStyle.blurple)
    async def esh_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response(button.label), ephemeral=True)
    
    @discord.ui.button(label='NAH', style=ButtonStyle.gray)
    async def nah_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response(button.label), ephemeral=True)

    @discord.ui.button(label='INFO', style=ButtonStyle.grey)
    async def info_callback(self, button, interaction):
        await interaction.response.send_message( 
                content=self.get_response(button.label), ephemeral=True)

    # must truncate it to 2000 characters
    def get_response(self, guess):
        if self.post['sdec'] == "None": 
            content = f"Unable to locate a top comment with a valid decision. {self.post['decision']}"
        elif guess == self.post['sdec']: 
            content = f"{guess} was **correct**! {self.post['decision']}"
        else: 
            content = f"{guess} was **incorrect**! {self.post['decision']}"
        if len(content) > 2000:
            content = content[:2000-3] + '...'
        return content

def setup(bot):
    bot.add_cog(Reddit(bot))