# wid-bot 

[![commits](https://badgen.net/github/commits/ericpretzel/wid-bot/main)](https://github.com/ericpretzel/wid-bot/commit/main)
[![last-commit](https://badgen.net/github/last-commit/ericpretzel/wid-bot/main)](https://github.com/ericpretzel/wid-bot/last-commit/main)

A Discord bot made in honor of Mr. Widmark. 

Main dependencies:
- [Python 3.9](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/) - used to manage misc. dependencies and run the bot
- [Pycord](https://github.com/Pycord-Development/pycord) - a [discord.py](https://github.com/Rapptz/discord.py) fork for interacting with the Discord API
- [Async PRAW](https://github.com/praw-dev/asyncpraw) - interacting with the Reddit API
- [Web3py](https://web3py.readthedocs.io/en/stable/#) - interacting with the blockchain
- Discord bot hosting service

## Features
wid-bot comes with a variety of amazing and fun commands to use, including, but not limited to...
Command      | Description
------------ | ------------
`/csgostats` | Retrieve a user's CS:GO stats
`/wordle`    | Play a game of Wordle
`/aita`      | Guess whether a Redditor is TA or not (very hard)
`/mint`      | Mint an NFT on the Widcoin blockchain

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute.

## Replication

*Note: wid-bot is intended for small private server use only because it uses the ["message content" privileged intent](https://support-dev.discord.com/hc/en-us/articles/4404772028055-Message-Content-Privileged-Intent-for-Verified-Bots). It will not work as a larger bot (100+ servers) without modification.*
1. **Create your own [Discord Application](https://discord.com/developers/applications). Make a [Reddit API](https://www.reddit.com/dev/api/) account as well.**  
For the NFT functionality, a [Moralis](https://moralis.io) API key and [Infura](https://infura.io) gateway token for the Ropsten testnet are required to access the blockchain. Furthermore, the NFT functionality uses real (test) Ethereum, so a Metamask (or similar) wallet with Ropsten Ethereum is required.  
*Access to the original ("OG") wid-bot application is restricted to members of Widmark Clan only.*

Make a Discord bot account for the application then add it to your server.
- Enable the "Message content intent"
- Scopes: `applications.commands` and `bot`
- Recommended permissions integer: `415038303296`

Keep the Discord bot token and Reddit secret/ID handy.

2. **Set up the code environment.**

`git clone` this repository, and make sure you have all the above dependencies installed. Pipenv will take care of the rest of them. 

Run the following commands inside the base directory of the project, which will store your  keys in a hidden file named `.env`. This is where sensitive information like the bot token and API keys will go. Replace the values below with your own personal values.
```
$ echo TOKEN=qwertyuiop >> .env
$ echo GUILD_ID=12345678 >> .env
$ echo REDDIT_SECRET=asdfghjkl >> .env
$ echo REDDIT_ID=zxcvbnm >> .env
$ echo INFURA_GATEWAY=ROPSTEN_GATEWAY_TOKEN >> .env
$ echo MORALIS_KEY=MORALIS_API_KEY >> .env
$ echo WID_ADDR=WALLET_PUBLIC_KEY >> .env
$ echo PRIVATE_KEY=WALLET_PRIVATE_KEY >> .env
```
These values are read and set up in [`config.py`](config.py). You can put them directly in the file instead, but make sure that those keys are never shared to the public because they can and will be stolen.

Install [`chromedriver 97.0.4692.71`](https://chromedriver.storage.googleapis.com/index.html?path=97.0.4692.71/) for headless browsing with [`selenium`](https://www.selenium.dev/). Either put the binary on PATH or in the base project directory. You may also need to install Google Chrome itself.

Finally, install the dependencies outlined in [`Pipfile`](Pipfile) and [`Pipfile.lock`](Pipfile.lock). 
```
$ pipenv install
```

3. **Host and run the bot.**

Use some hosting service to host the code of your bot. There's plenty of options out there. If you followed the steps above, wid-bot should be able to run right away.
```
$ pipenv run python3 bot.py
``` 
If everything works as it should, it should show something like this:
```
Loading .env environment variables…
wid is loading...
loading extension.[filename]... done (for all files in extension folder)
wid is ready!
```
and the bot should be online. Woo!
