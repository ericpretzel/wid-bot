"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Prototype smart contract for the first Widcoin-based NFT collection
"""
from unittest import result
from PIL import Image, ImageChops
from io import BytesIO
import discord
import config
import sqlite3
import web3
from web3 import Web3
from random import randint
import requests

def gen_img():
    """
    Generates new image to be used as NFT
    """
    colors = tuple(randint(0,255) for _ in range(3))
    response = requests.get(config.BASE_URL, stream=True)
    base = Image.open(response.raw).resize((config.NFT_SIZE, config.NFT_SIZE))
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

def mint_nft(addr, url):
    """
    Mints an NFT on the Ethereum blockchain with the given image and transfers to given user
    """
    pass
    # w3 = Web3(Web3.HTTPProvider(config.INFURA_GATEWAY))
    # contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.ABI)
    # contract.functions.mint(addr, url).transact()

def get_last_nft(address):
    """
    Returns the most recently acquired NFT by the given user address or None if none exists.
    """
    url = f'https://deep-index.moralis.io/api/v2/{address}/nft?chain=ropsten&format=decimal'
    headers = {'accept': 'application/json', 'X-API-KEY': config.MORALIS_KEY}
    response = requests.get(url, headers=headers)
    if response.ok:
        nfts = response.json()['result']
        if len(nfts) > 0:
            return nfts[0]['token_address'], nfts[0]['token_id']
    return None, None
