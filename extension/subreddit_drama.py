"""
subredditdrama.py
Author: Hirod Nazari
Uses get_subreddit_drama() in reddit_scraper.py to find top 5 posts on r/SubredditDrama

Note: With heavy inspiration from Kai (Emphasis on heavy)
"""

import config
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from discord.commands import slash_command
from util.reddit_scraper import get_aita

class DramaView(View):
    def __init__(self, post):
        super().__init__()
        self.post = post

class DRAMA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.GUILD_ID],
        description="What's the latest drama on Reddit?")
    async def aita(self, ctx: discord.ApplicationContext):
        try:
            await ctx.defer()
            post = await get_aita()
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

        await ctx.respond(embed=embed, view=DramaView(post))

def setup(bot):
    bot.add_cog(DRAMA(bot))
    