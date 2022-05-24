import os
# Discord bot access token. Located in .env file in base directory.
TOKEN = os.environ['TOKEN']
# You get these from developer settings in reddit, ask kai to get added as developer
REDDIT_SECRET = os.environ['REDDIT_SECRET']
REDDIT_ID = os.environ['REDDIT_ID']

# the ID of the server that wid-bot is on
GUILD_ID = int(os.environ['GUILD_ID'])

# folder that all data files are stored in
DATA_FOLDER = 'data'

# Persistent data storage
DB_FILE = 'config.db'

# NFT related
NFT_SIZE = 600
INFURA_GATEWAY = os.environ['INFURA_GATEWAY']
BASE_URL = 'https://cdn.discordapp.com/attachments/915513848059027457/945195853725978644/unknown.png'
CONTRACT_ADDRESS = 'FIXME'
ABI = {}
MORALIS_KEY = os.environ['MORALIS_KEY']

# Wordle related
WORDLE_WORD_LIST = os.path.join(DATA_FOLDER, 'wordle-word-list.txt')
FIVE_LETTER_WORDS = os.path.join(DATA_FOLDER, 'five-letter-words.txt')

# Default emoji mappings found here: 
# https://raw.githubusercontent.com/Kevinpgalligan/EmojipastaBot/master/src/emojipasta/data/emoji-mappings.json
EMOJI_MAPPINGS = os.path.join(DATA_FOLDER, 'emoji-mappings.json')

# Demons storage
DEMONS_FOLDER = os.path.join(DATA_FOLDER, 'demons', )