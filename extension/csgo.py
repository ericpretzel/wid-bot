import config
import discord
from discord.ext import commands
from discord.commands import slash_command
import requests
import json
import pprint

stats = [
    'timePlayed',
    'kills',
    'deaths',
    'kd',
    'damage',
    'bombsPlanted',
    'bombsDefused',
    'mvp',
    'wins',
    'ties',
    'losses',
    'wlPercentage',
    'roundsPlayed',
    'headshotPct'
]
def _get_stat(r, stat):
    return r['data']['segments'][0]['stats'][stat]['value']

def _adr(r):
    return int(_get_stat(r, 'damage')) / int(_get_stat(r, 'roundsPlayed'))

class CSGO(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID])
    async def csgostats(self, ctx: discord.ApplicationContext, user: str):
        url = f'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{user}'
        headers = {'TRN-Api-Key': config.TRN_API_KEY}
        r = requests.get(url=url, headers=headers).json()

        embed=discord.Embed(title=f"CS:GO stats for user {user}", description="from tracker.gg")
        embed.add_field(name="K/D", value=int(_get_stat(r, 'kills'))/int(_get_stat(r, 'deaths')), inline=True)
        embed.add_field(name="Win %", value=_get_stat(r, 'wlPercentage'), inline=True)
        embed.add_field(name='ADR', value=_adr(r), inline=True)
        embed.add_field(name="Headshot %", value=_get_stat(r, 'headshotPct'), inline=True)
        embed.add_field(name="Time Played", value=_get_stat(r, 'timePlayed'), inline=True)
        
        await ctx.respond(embed=embed)




def setup(bot):
    bot.add_cog(CSGO(bot))