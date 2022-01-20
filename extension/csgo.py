import config
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from scraper import get_stats

# display value : json value
stat_values = {
    'ADR': 'adr',
    'HS %': 'hs',
    'K/D': 'kpd',
    'Rating': 'rating',
    'Win %': 'wr'
}

class CSGO(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID], 
        description="Retrieve a player's CSGO stats.")
    async def csgostats(self,
        ctx: discord.ApplicationContext,
        url: Option(str, "Steam profile URL (or custom URL name)", required=True)):
        
        if '/' in url[:-1]:
            if url[-1] == '/':
                url = url[:-1]
            user = url[url.rindex('/')+1:]
        else: user = url

        await ctx.defer() # need to defer so the command doesn't time out

        try:
            stats = get_stats(user)
        except Exception as e:
            return await ctx.respond(e.args[0])

        embed=discord.Embed(title=f"CS:GO stats for {stats['nickname']}", description="from csgostats.gg")
        for k, v in stat_values.items():
            embed.add_field(name=k, value=stats['overall'][v], inline=True)
        embed.set_thumbnail(url=stats['thumbnail'])

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(CSGO(bot))