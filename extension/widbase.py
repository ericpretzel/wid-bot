import sqlite3
import config
import discord
import datetime
from discord.ext import commands, tasks
import discord.utils
from discord.commands import slash_command, Option

class Widbase(commands.Cog):
    """
    Manages the widmark clan database
    """
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.update_widbase.start()

    @tasks.loop(hours=8)
    async def update_widbase(self):
        await self.bot.wait_until_ready()
        print('Updating messages in database...')
        conn = sqlite3.connect(config.DB_FILE)
        # create messages table if it doesn't exist
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                message_id integer PRIMARY KEY,
                author_id  integer NOT NULL,
                channel_id integer NOT NULL,
                timestamp  integer NOT NULL,
                content    text
            );"""
        )
        conn.commit()

        # get latest time from stored messages
        cur = conn.execute('SELECT MAX(timestamp) FROM messages;')
        guild = self.bot.get_guild(config.GUILD_ID)
        latest_message = datetime.datetime.fromtimestamp(cur.fetchone()[0] or guild.created_at.timestamp(), tz=datetime.timezone.utc)

        # gather and insert new messages since last time
        for channel in guild.text_channels:
            async for message in channel.history(limit=None, after=latest_message):
                values = (message.id, message.author.id, channel.id, int(message.created_at.timestamp()), message.content)
                conn.execute(f'INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?);', values)
                conn.commit()
        print('Successfully updated messages in database.')
        conn.close()

def setup(bot):
    bot.add_cog(Widbase(bot))
