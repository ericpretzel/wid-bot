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

# fonts folder
FONT_FOLDER = os.path.join(DATA_FOLDER, 'font')

# Persistent data storage
DB_FILE = os.path.join(DATA_FOLDER, 'config.db')

# NFT related
NFT_SIZE = 600
INFURA_GATEWAY = os.environ['INFURA_GATEWAY']
BASE_URL = 'https://cdn.discordapp.com/attachments/915513848059027457/945195853725978644/unknown.png'
CONTRACT_ADDRESS = '0xE551386387B1293a738FB5b0aaB10592d13473A2'
WID_ADDR = os.environ['WID_ADDR']
PRIVATE_KEY = os.environ['PRIVATE_KEY']
MORALIS_KEY = os.environ['MORALIS_KEY']
ABI_PATH = os.path.join(DATA_FOLDER, 'abi.json')

# Wordle related
WORDLE_WORD_LIST = os.path.join(DATA_FOLDER, 'wordle-word-list.txt')
FIVE_LETTER_WORDS = os.path.join(DATA_FOLDER, 'five-letter-words.txt')

# Default emoji mappings found here: 
# https://raw.githubusercontent.com/Kevinpgalligan/EmojipastaBot/master/src/emojipasta/data/emoji-mappings.json
EMOJI_MAPPINGS = os.path.join(DATA_FOLDER, 'emoji-mappings.json')

# Sillyfier data storage
SILLY_FOLDER = os.path.join(DATA_FOLDER, 'silly')
SILLY_JJK = os.path.join(SILLY_FOLDER, 'jjk')

# fonts
FONT_COMIC_SANS = os.path.join(FONT_FOLDER, 'comic-sans.ttf')
