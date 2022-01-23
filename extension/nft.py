"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Infrastructure for the Widmark Clan crypto branch NFT exchange
"""

import config
import discord
from discord.commands import slash_command
from discord.ext import commands
from util.smart_contract import ensure_wallet, mint_nft, nft, show, own_nft

class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID], 
        description="Retrieve a user's NFT wallet.")
    async def wallet(self,
        ctx: discord.ApplicationContext,
        user:  discord.Member=None, nft_id: int=None):
        
        if not user: user = ctx.author

        user_wallet = ensure_wallet(user, config)

        if(user_wallet):
            nft = user_wallet[(nft_id or -1)% len(user_wallet)]
            embed = discord.Embed(title=f"{user.nick or user.name}\'s latest NFT!", description=f'Chance to get: {nft["rarity"]}%')
            file = show(nft, config)
            embed.set_image(url=f'attachment://{nft["address"]}.png')
            embed.set_footer(text=str(nft["address"]))
            await ctx.respond(embed=embed, file=file)

        else:
            await ctx.respond(f'{user.nick or user.name} has no NFTs!')

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID], 
        description="Mint an NFT on the Widcoin blockchain.")
    async def mint(self,
        ctx: discord.ApplicationContext):
        try:
            nft = mint_nft(config)
            user = ctx.author

            own_nft(user, nft, config)

            embed = discord.Embed(title=f"{user.nick or user.name} just minted a new NFT!", description=f'Chance to get: {nft["rarity"]}%')
            file = show(nft, config)
            embed.set_image(url=f'attachment://{nft["address"]}.png')
            embed.set_footer(text=str(nft["address"]))
            await ctx.respond(embed=embed, file=file)
        except Exception as e:
            print(e)
            await ctx.respond('A skill issue prevented the minting of an NFT')


def setup(bot):
    bot.add_cog(Crypto(bot))