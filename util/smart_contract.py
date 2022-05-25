"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Prototype smart contract for the first Widcoin-based NFT collection
"""
from unittest import result
from PIL import Image, ImageChops
import discord
import config
import sqlite3
import web3
from web3 import Web3
from random import randint
import json
import base64
import aiohttp
from io import BytesIO

async def gen_img():
    """
    Generates new image to be used as NFT
    """
    colors = tuple(randint(0,255) for _ in range(3))
    async with aiohttp.ClientSession() as session:
        async with session.get(config.BASE_URL) as resp:
            if resp.status == 200:
                bin_img = await resp.read()
                base = Image.open(BytesIO(bin_img)).resize((config.NFT_SIZE, config.NFT_SIZE))
                tint = Image.new(mode='RGBA', size=(config.NFT_SIZE, config.NFT_SIZE), color=colors)
                return ImageChops.multiply(base, tint)

def get_address(id):
    """
    Gets the Metamask address of given user or returns None if none exists.
    """
    con = sqlite3.connect(config.DB_FILE)
    try:
        cursor = con.execute(f'SELECT address FROM users WHERE uid="{id}"')
        address = next(cursor)[0]
        return address
    except Exception as e:
        print(e)
        return None

def mint_nft(addr, img_url):
    """
    Mints an NFT on the Ethereum blockchain with the given image and transfers to given user
    """
    with open(config.ABI_PATH, 'rt') as f:
        abi = json.load(f)['abi']
    uri = 'data:application/json;base64,' \
        + base64.b64encode(bytes('{"name": "wid","description": "Widmark NFTs","image": "' \
          + img_url + '"}', 'utf8')).decode('ascii')
    w3 = Web3(Web3.HTTPProvider(config.INFURA_GATEWAY))
    contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=abi)
    tx = contract.functions.safeMint(uri, addr)\
        .buildTransaction({'nonce': w3.eth.getTransactionCount(config.WID_ADDR)})
    signed_tx = w3.eth.account.signTransaction(tx, private_key=config.PRIVATE_KEY)
    w3.eth.sendRawTransaction(signed_tx.rawTransaction)

async def get_last_nft(address):
    """
    Returns the most recently acquired NFT by the given user address or None if none exists.
    """
    url = f'https://deep-index.moralis.io/api/v2/{address}/nft?chain=ropsten&format=decimal'
    headers = {'accept': 'application/json', 'X-API-KEY': config.MORALIS_KEY}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                nfts = await resp.json()
                if len(nfts['result']) > 0:
                    return nfts['result'][0]['token_address'], nfts['result'][0]['token_id']
    return None, None
