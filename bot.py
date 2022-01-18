import discord
import config
import os

bot = discord.Bot()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('test'))

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