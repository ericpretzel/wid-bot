import asyncio
import config
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from util.cs_scraper import get_stats

# display value : json value
stat_values = {
    'ADR': 'adr',
    'HS %': 'hs',
    'K/D': 'kpd',
    'Rating': 'rating',
    'Win %': 'wr',
    'Games Played': 'games',
    'CS:GO Rank': 'csgo_rank',
    'Premier Rank': 'premier_rank'
    # thumbnail
}

class CounterStrike(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.GUILD_ID], 
        description="Retrieve a player's CS2 stats.")
    async def csstats(self,
        ctx: discord.ApplicationContext,
        url: Option(str, "Steam profile URL (or custom URL name)", required=True)):

        await ctx.defer()

        if '/' in url[:-1]:
            if url[-1] == '/':
                url = url[:-1]
            user = url[url.rindex('/')+1:]
        else: user = url

        try:
            stats = await get_stats(user)
        except Exception as e:
            return await ctx.respond(str(e))

        embed=discord.Embed(title=f"Counter Strike stats for {stats['nickname']}", description="from csstats.gg")
        for k, v in stat_values.items():
            embed.add_field(name=k, value=stats.get(v, "?"), inline=True)
        embed.set_thumbnail(url=stats['thumbnail'])

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(CounterStrike(bot))