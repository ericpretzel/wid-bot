# Contributing
Thanks for offering to contribute to wid-bot and helping to make it the greatest bot on Discord.

If you want ideas for something to work on, check if there are any open [issues](https://github.com/ericpretzel/wid-bot/issues).

First, make sure you are familiar with `pycord`. They have relatively up-to-date [documentation](https://docs.pycord.dev/en/master/) online. It changes a lot though because there are new features constantly being added.

## Adding new commands
Commands must always be slash commands because ~~[this is what Discord wants](https://en.wikipedia.org/wiki/Nineteen_Eighty-Four)~~.

All current commands are located inside cogs and it is probably best to keep it like that. Cogs are groups of commands (related to each other) that the bot automatically detects and loads. All cogs are located in the [`extension`](extension) directory and are automatically loaded in [`bot.py`](https://github.com/ericpretzel/wid-bot/blob/5501c4b2fc780fde49af4a20cbaed3d343850332/bot.py#L27-L35) during startup. 
- **Cogs must have unique names.**
- Cogs must have a global `setup` function (look at existing cogs to see how it should look) or loading it will throw an error.

## Testing
It is necessary that you test your bot to make sure it works before pushing the changes to any branch. You also don't want to take down the main bot every time you're trying to make changes. A solution to this is to make a separate application/bot for testing. This repo was made such that testing should not require that many changes.

The bot account will at the very least use a different token. You'll need to change the `TOKEN` environment variable. Since testing does not need to be up 24/7, putting the testing bot token on your personal development computer's `.env` file and keeping the main bot token on your hosting service's `.env` file is a good idea.

I also put the testing bot on a different server; in that case, you will also need to change the `GUILD_ID` environment variable.

Rarely, large changes such as file restructuring may need additional testing to make sure it works on the server, so in that case it may need to go down. That's fine as long as it isn't too often.

## Pull requests
If you are a member of Widmark clan (a contributor), just make a new branch and push the changes to that branch. Make a pull request to merge it into `main`. We'll review it ASAP! *Pushing directly to `main` (unless you are Eric) is disabled.*

If you are not a member of Widmark clan, you will need to make a fork of the repository and add your changes there. Then you can make a pull request as usual.
