import discord
import config

bot = discord.Bot()

@bot.slash_command(guild_ids=[config.WIDMARK_CLAN_GUILD_ID])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    if msg.author.id == '162691839164547072':
        await msg.channel.send('why dont you code urself some bitches')

    if 'nft' in msg.content.lower():
        await msg.channel.send('OMW TO BUY')

bot.run(config.TOKEN)
