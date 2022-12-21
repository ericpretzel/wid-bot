import discord
from discord.ext import commands
import config
import os

print('wid is loading...')

bot = commands.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('CS:GO with widmark clan'))
    print('wid is ready!')

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, exc: discord.ApplicationCommandError):
    return await ctx.respond(exc)

# currently won't work: slash commands cannot be reloaded.
# hopefully will be changed in the future
@bot.slash_command(guild_ids=[config.GUILD_ID])
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
    print(f'loading extension.{extension}... ', end='')
    try:
        bot.load_extension('extension.' + extension)
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension {extension}\n{exc}')
    print('done')

bot.run(config.TOKEN)