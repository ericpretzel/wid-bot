import config
import discord
from discord.commands import slash_command
from discord.ext import commands
from PIL import Image, ImageChops
from numpy.random import normal, randint
from os import listdir

class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class NFT:
        def __init__(self, base, transformation):
            self.base = base
            self.transformation = transformation
            color = 1
            #widmark clan super advanced smart contract
            self.rarity = randint(0, 100)

            for v in transformation: color*=v
            #widmark clan super advanced nft hashing algorithm
            self.address = hex(int(0x1000000)+v)    

        def show():
            base = Image.open(constants.base)
            tint = Image.new(mode='RGB', size=(config.NFT_SIZE, config.NFT_SIZE), color = colors)
            out = ImageChops.multiply(base, tint)

            with BytesIO() as export:
                out.save(export, 'png')
                export.seek(0)
                return discord.File(fp=export, filename=f'{self.address}.png')

    def ensure_wallet(who):
        if(not config.wallet):
            config.wallet = {}
        if(not config.wallet[who.id]):
            config.wallet[who.id] = []
        return config.wallet[who.id]

    def mint_nft():
        """
        Widmark clan super advanced NFT smart contract
        """
        colors = [int(normal(255/2, 255/6))%255 for _ in range(3)]
        if config.nfts > 255**3:
            raise AttributeError("All nft's have been minted!")        
        return NFT(constants.base, colors)



    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID], 
        description="Retrieve a user's NFT wallet.")
    async def wallet(self,
        ctx: discord.ApplicationContext,
        who:  discord.Member=None, nft_id: int=None):
        
        if not who: who = ctx.author

        await ctx.defer()

        user_wallet = ensure_wallet(who)

        if(user_wallet):
            nft = user_wallet[(nft_id%len(user_wallet)) or -1]
            embed = discord.Embed(title=f"{who.nick}\'s NFT wallet", description="on the Widcoin blockchain")
            file = nft.show()
            embed.set_image(url="attachment://output.png")
            embed.set_footer(nft.address)
            await ctx.respond(embed=embed)

        else:
            await ctx.respond(f'{who.nick} has no NFTs!')

    @slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID], 
        description="Retrieve a user's NFT wallet.")
    async def mint(self,
        ctx: discord.ApplicationContext):
        try:
            nft = mint_nft()
            user_wallet = ensure_wallet(ctx.author)
            user_wallet.append(nft)

            embed = discord.Embed(title=f"{who.nick}\'s new NFT!", description=f"Rarity: {nft.rarity}%")
            file = nft.show()
            embed.set_image(url="attachment://output.png")
            embed.set_footer(nft.address)
            await ctx.respond(embed=embed)
        except:
            await ctx.respond('A skill issue prevented the minting of an NFT')


def setup(bot):
    bot.add_cog(CSGO(bot))