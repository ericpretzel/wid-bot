import discord
import config

bot = discord.Bot()

@bot.slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.event
async def on_message(msg):
    if msg.author.bot: return

    if 'nft' in msg.content.lower():
        await msg.channel.send('nft bad')

bot.run(config.TOKEN)