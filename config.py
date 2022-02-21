import os
# Discord bot access token. Located in .env file in base directory.
TOKEN = os.environ['TOKEN']
# You get these from developer settings in reddit, ask kai to get added as developer
REDDIT_SECRET = os.environ['REDDIT_SECRET']
REDDIT_ID = os.environ['REDDIT_ID']

# hard-coded channel/server IDs
WIDMARK_CLAN_GUILD_ID = 842270794562535434

# NFT related
WALLET = 'data/wallet.json'
NFT_SIZE = 600
PREFIX = 'https://ipfs.io/ipfs/'
BASE = 'QmWrHFYZarTP2b1qCzG7xB45C7P2f8NvEczUfKDgiv3uEs'

# Wordle related
WORDLE_WORD_LIST = 'data/wordle-word-list.txt'
FIVE_LETTER_WORDS = 'data/five-letter-words.txt'

# Bad words
BAD_WORDS = ['henlo']