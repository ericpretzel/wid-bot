"""
smart_contract.py 
By Lance Mathias <l.a.mathia1@gmail.com>
Prototype smart contract for the first Widcoin-based NFT collection
"""
from PIL import Image, ImageChops
from io import BytesIO
import discord
import config
import json
from random import randint
import requests

def ensure_wallet(user):
    try:
        with open(config.WALLET, 'rt') as w:
            nft_wallet = json.load(w)
        return nft_wallet.get(str(user.id))
    except FileNotFoundError:
        with open(config.WALLET, 'wt') as w:
            w.write("{}")

def own_nft(user, nft):
    try:
        with open(config.WALLET, 'rt') as w:
            nft_wallet = json.load(w)
    except FileNotFoundError:
        with open(config.WALLET, 'wt') as w:
            w.write("{}")
        nft_wallet = {}
    if(nft_wallet.get(str(user.id)) is None):
        nft_wallet[str(user.id)] = []
    nft_wallet[str(user.id)].append(nft)
    with open(config.WALLET, 'wt') as w:
        json.dump(nft_wallet, w)

def mint_nft():
    """
    Widmark clan super advanced NFT smart contract
    """
    colors = tuple(randint(0,255) for _ in range(4))
    return nft(config.BASE, colors)

def nft(_base, _colors):
    color = 1
    for v in _colors: color *= v
    return {"base":_base, "colors": _colors, "rarity": randint(1,100), "address":hex(int(0x100000000)+color)}

def show(nft):
    response = requests.get(config.PREFIX + config.BASE, stream=True)

    base = Image.open(response.raw)
    tint = Image.new(mode='RGBA', size=(config.NFT_SIZE, config.NFT_SIZE), color = tuple(nft["colors"]))
    out = ImageChops.multiply(base, tint)

    with BytesIO() as export:
        out.save(export, 'png')
        export.seek(0)
        return discord.File(fp=export, filename=f'{nft["address"]}.png')