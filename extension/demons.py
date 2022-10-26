import config
import discord
from discord.ext import commands, tasks
from discord.commands import user_command
from discord.utils import escape_mentions
import sqlite3
import util.demon_manager as dm

class Demons(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.summon_demons.start()

    @user_command(name="Unleash Demons", guild_ids=[config.GUILD_ID])
    async def demons(self, ctx: discord.ApplicationContext, mem: discord.Member):
        message = f"**{mem.display_name}'s demons:**\n"
        try:
            message += dm.generate_sentences(mem.id, 15)
        except dm.ModelNotFoundException:
            return await ctx.respond('These demons have not been summoned yet...', ephemeral=True)
        message = escape_mentions(message)
        if len(message) > 2000:
            message = message[:2000-3] + '...'
        await ctx.respond(message)

    @tasks.loop(hours=12)
    async def summon_demons(self):
        """
        Fetches every single message from the server, then groups them by user -> messages
        """
        await self.bot.wait_until_ready()
        con = sqlite3.connect(config.DB_FILE)
        try:
            cur = con.execute("""SELECT author_id, content FROM messages""")
            messages = cur.fetchall()
        except:
            print('could not generate demons, likely because the messages table does not exist (yet)')
            return
        finally:
            con.close()
        
        data = {}
        for entry in messages:
            author, msg = entry[0], entry[1]
            if len(msg) > 6 and not msg.startswith('http') and not msg.startswith(':'):
                data.setdefault(author, []).append(msg)
        
        dm.generate_demon_report(data)

def setup(bot):
    bot.add_cog(Demons(bot))
