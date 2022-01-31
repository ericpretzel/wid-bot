"""
Author: Kai (Not Eric (Not Lance (Not Russell)))
"""

from distutils.log import info
import config
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from discord.commands import slash_command
from util.reddit_scraper import get_aita

class AITA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID],
        description="Are they the Asshole?")
    async def aita(self, ctx: discord.ApplicationContext):
        try:
            post = await get_aita()
        except Exception as e:
            return await ctx.respond('Unable to find an asshole. Try the mirror.', ephemeral=True)  
        
        embed = discord.Embed(
            title=post['title'],
            url=f"https://reddit.com{post['link']}",
            description=post['desc']
        )
        embed.set_footer(text=f"{post['upvotes']} upvotes")
        embed.set_author(name=post['author'])

        yta_button = Button(label='YTA', style=ButtonStyle.red)
        nta_button = Button(label='NTA', style=ButtonStyle.green)
        esh_button = Button(label='ESH', style=ButtonStyle.blurple)
        info_button = Button(label='INFO', style=ButtonStyle.grey)
        view = View()
        view.add_item(yta_button)
        view.add_item(nta_button)
        view.add_item(esh_button)
        view.add_item(info_button)
        

        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(AITA(bot))