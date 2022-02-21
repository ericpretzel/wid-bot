from http import client
import discord
from discord.ext import commands
import config
import os

print('wid is loading...')

bot = commands.Bot()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('CS:GO with widmark clan'))
    print('wid is ready!')

@client.event
async def on_message(ctx, message):
    '''
    Bad words filter
    Deletes any messages in BAD_WORDS list in the config
    '''
    if any(word in message.content for word in config.BAD_WORDS):
        await message.delete()
        await ctx.send('UwU don\'t use that word pwease!')
    await ctx.process_message(message)

# currently won't work: slash commands cannot be reloaded.
# hopefully will be changed in the future
@bot.slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID])
@commands.is_owner()
async def reload(ctx: discord.ApplicationContext, ext: str):
    try:
        bot.reload_extension('extension.' + ext)
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to reload extension {ext}\n{exc}')
    await ctx.respond('Done')

for file in os.listdir('extension'):
    if not file.endswith('.py'):
        continue
    extension = file[:-3]
    try:
        bot.load_extension('extension.' + extension)
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {extension}\n{exc}')

bot.run(config.TOKEN)