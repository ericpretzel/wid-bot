import os
# Discord bot access token. Located in .env file in base directory.
TOKEN = os.environ['TOKEN']
# You get these from developer settings in reddit, ask kai to get added as developer
REDDIT_SECRET = os.environ['REDDIT_SECRET']
REDDIT_ID = os.environ['REDDIT_ID']

# the ID of the server that wid-bot is on
GUILD_ID = int(os.environ['GUILD_ID'])

# folder that all data files are stored in
DATA_FOLDER = 'data/'

# NFT related
WALLET = DATA_FOLDER + 'wallet.json'
NFT_SIZE = 600
PREFIX = 'https://ipfs.io/ipfs/'
BASE = 'QmWrHFYZarTP2b1qCzG7xB45C7P2f8NvEczUfKDgiv3uEs'

# Wordle related
WORDLE_WORD_LIST = DATA_FOLDER + 'wordle-word-list.txt'
FIVE_LETTER_WORDS = DATA_FOLDER + 'five-letter-words.txt'

# Default emoji mappings found here: 
# https://raw.githubusercontent.com/Kevinpgalligan/EmojipastaBot/master/src/emojipasta/data/emoji-mappings.json
EMOJI_MAPPINGS = DATA_FOLDER + 'emoji-mappings.json'
