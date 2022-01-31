import os
# Discord bot access token. Located in .env file in base directory.
TOKEN = os.environ['TOKEN']

# hard-coded channel/server IDs
WIDMARK_CLAN_GUILD_ID = 842270794562535434
PRIVATE_PORN_CHANNEL_ID = 882074562529988649

# NFT related
WALLET = 'data/wallet.json'
NFT_SIZE = 600
PREFIX = 'https://ipfs.io/ipfs/'
BASE = 'QmWrHFYZarTP2b1qCzG7xB45C7P2f8NvEczUfKDgiv3uEs'

# Wordle related
WORDLE_WORD_LIST = 'data/wordle-word-list.txt'
FIVE_LETTER_WORDS = 'data/five-letter-words.txt'

# users that are noobs
blacklist = {
    'YERBA': 171396895661359104,
    'SAMMICH': 215276133875318785,
    'ERAKAI': 215272766977474561
}