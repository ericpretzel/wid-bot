"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Infrastructure for the Widmark Clan crypto branch NFT exchange
"""

from tkinter.messagebox import NO
from urllib import response
import config
import discord
from discord import Option
import web3
from web3 import Web3
import sqlite3
from discord.ext import commands
from util.smart_contract import gen_img, get_address, mint_nft, get_last_nft
from io import BytesIO
import requests
import ast

counter = 0

class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    nft_group = discord.SlashCommandGroup('nft', 'Commands related to NFTs', guild_ids=[config.GUILD_ID])

    @nft_group.command(description="Link a user's Metamask adress to Wid bot.")
    async def connect(self, ctx: discord.ApplicationContext, address: str):
        w3 = Web3(Web3.HTTPProvider(config.INFURA_GATEWAY))

        try:
            bal = Web3.fromWei(w3.eth.get_balance(address), 'ether')
        except web3.exceptions.InvalidAddress:
            await ctx.respond('Invalid Metamask address!', ephemeral=True)
            return

        try:
            con = sqlite3.connect(config.DB_FILE)
            con.execute('CREATE TABLE IF NOT EXISTS users (uid TEXT PRIMARY KEY, address TEXT NOT NULL);')
            con.commit()

            # Insert user-address pair into table - ONLY INSERT AFTER VALIDATION
            con.execute(f'INSERT OR IGNORE INTO users VALUES ("{ctx.author.id}", "{address}")')
            con.commit()
            con.execute(f'UPDATE users SET address="{address}" WHERE uid="{ctx.author.id}"')
            con.commit()
        except Exception as e:
            print(e)
            await ctx.respond('A skill issue prevented address storage', ephemeral=True)
            return
        await ctx.respond('Address successfully recorded!', ephemeral=True)

    @nft_group.command(description="Mint an NFT on the Widcoin blockchain.")
    async def mint(self, ctx: discord.ApplicationContext):
        global counter
        address = get_address(ctx.author.id)
        if address is None:
            await ctx.respond('Connect your wallet to Wid first!', ephemeral=True)
            return

        try:
            img = gen_img()
            counter += 1
            with BytesIO() as export:
                img.save(export, 'png')
                export.seek(0)
                imgFile = discord.File(fp=export, filename=f'{counter}.png')
            preview = discord.Embed(title='NFT Preview')
            preview.set_image(url=f'attachment://{counter}.png')
            preview.description = 'Minting...'
            msg = await ctx.respond(embed=preview, file=imgFile)

        except Exception as e:
            print(e)
            msg_content = await msg.original_message()
            await msg_content.delete()
            await ctx.respond('A skill issue prevented NFT generation', ephemeral=True)
            return

        try:
            msg_content = await msg.original_message()
            img_url = msg_content.embeds[0].image.url
            mint_nft(address, img_url)
            preview.title = f'{ctx.author.nick or ctx.author.name}\'s new NFT!'
            etherscan_url = f'https://ropsten.etherscan.io/address/{address}'
            preview.description = f'[{address}]({etherscan_url})'
            await msg.edit_original_message(embed=preview)
        except Exception as e:
            print(e)
            await msg_content.delete()
            await ctx.respond('A skill issue prevented NFT generation', ephemeral=True)

    @nft_group.command(description="Retrieve specified NFT or user's latest NFT (Ropsten only).")
    async def view(self, ctx: discord.ApplicationContext,
        user: Option(discord.Member, "Search for user's NFTs", required = False, default = None),
        address: Option(str, "NFT contract address", required = False, default = None),
        id: Option(int, "NFT id", required = False, default = None)):
        if address is None or id is None:
            user = user or ctx.author
            usr_address = get_address(user.id)
            if usr_address is None:
                await ctx.respond('User does not have a wallet!', ephemeral=True)
                return
            address, id = get_last_nft(usr_address)
        url = f'https://deep-index.moralis.io/api/v2/nft/{address}/{id}?chain=ropsten&format=decimal'
        headers = {'accept': 'application/json', 'X-API-KEY': config.MORALIS_KEY}
        response = requests.get(url, headers=headers)
        if response.ok:
            metadata = ast.literal_eval(response.json()['metadata'])
            img_url = metadata['image']
            etherscan_url = f'https://ropsten.etherscan.io/address/{address}'
            owner = response.json()['owner_of']
            
            # Hack around moralis formatting weirdness
            owner = user.nick or user.name if usr_address.lower() == owner.lower() else owner
            
            embed = discord.Embed(title=f'{owner}\'s NFT!')
            embed.set_image(url=img_url)
            embed.description = f'[{address}]({etherscan_url})'
            await ctx.respond(embed=embed)
            return
        print(f'Invalid combo:{user}, {address}, {id}')
        await ctx.respond('NFT not found!', ephemeral=True)

def setup(bot):
    bot.add_cog(Crypto(bot))