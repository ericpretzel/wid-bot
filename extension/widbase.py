import aiosqlite
import config
import discord
import datetime
from discord.ext import commands, tasks
import discord.utils
from discord.commands import slash_command, Option
import io
import altair as alt
import altair_saver as alt_saver
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import collections

class Widbase(commands.Cog):
    """
    Manages the widmark clan database
    """
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.update.start()
    
    stats = discord.SlashCommandGroup(name='stats', description='Commands related to the widbase', guild_ids=[config.GUILD_ID])
    
    @stats.command(name='count', description='Get a chart showing how many messages people have sent.')
    async def message_count(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        async with aiosqlite.connect(config.DB_FILE) as con:
            async with await con.execute(
                """
                SELECT author_id, COUNT(*) FROM messages GROUP BY author_id;
                """) as cur:
                source = pd.DataFrame(data=await cur.fetchall(), columns=['author_id', 'COUNT(*)'])

        id_to_username = {}
        for author_id in source['author_id']:
            user = await self.bot.get_or_fetch_user(author_id)
            if user and not user.bot:
                id_to_username[author_id] = user.display_name
        source['author_id'] = source['author_id'].apply(id_to_username.get)
        source.dropna(inplace=True)
        chart = alt.Chart(source).mark_bar().encode(
            x=alt.X('author_id', title='User', type='nominal', sort='y'),
            y=alt.Y('COUNT(*)', title='Messages sent')
        )
        file = io.BytesIO(alt_saver.save(chart=chart, fmt='png'))
        file.seek(0)
        return await ctx.respond(file=discord.File(fp=file, filename='count.png'))
    
    @stats.command(name='wordcloud', description='Generate a word cloud for a specified user, or for the entire server if unspecified.')
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.default)
    async def word_cloud(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        await ctx.defer()
        # adds WHERE clause if user is specified
        async with aiosqlite.connect(config.DB_FILE) as con:
            if user:
                messages = await con.execute_fetchall(
                    "SELECT LOWER(content) FROM messages WHERE author_id=(?);",
                    (user.id,)
                )
            else:
                messages = await con.execute_fetchall(
                    "SELECT LOWER(content) FROM messages;"
                )
    
        frequencies = {}
        for row in messages:
            msg = row[0].strip().split(' ')
            for word in msg:
                if word not in STOPWORDS:
                    frequencies[word] = frequencies.get(word, 0) + 1

        wordcloud = WordCloud(width=400, height=400, scale=2,
                                max_words=100,
                                background_color='white',
                                min_font_size=10).generate_from_frequencies(frequencies=frequencies)
        plt.figure(figsize = (8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.tight_layout(pad=0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return await ctx.respond(f"{user.display_name if user else 'The server'}'s word cloud:", file=discord.File(fp=buf, filename='cloud.png'))

    @tasks.loop(hours=8)
    async def update(self):
        print('Updating messages in database...')
        # create messages table if it doesn't exist
        async with aiosqlite.connect(config.DB_FILE) as con:
            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    message_id integer PRIMARY KEY,
                    author_id  integer NOT NULL,
                    channel_id integer NOT NULL,
                    timestamp  integer NOT NULL,
                    content    text
                );"""
            )
            await con.commit()

            # get latest time from stored messages
            async with await con.execute('SELECT MAX(timestamp) FROM messages;') as cur:
                guild = await self.bot.fetch_guild(config.GUILD_ID)
                latest_message = datetime.datetime.fromtimestamp((await cur.fetchone())[0] or guild.created_at.timestamp(), tz=datetime.timezone.utc)

            # gather and insert new messages since last time
            for channel in guild.text_channels:
                async for message in channel.history(limit=None, after=latest_message):
                    values = (message.id, message.author.id, channel.id, int(message.created_at.timestamp()), message.content)
                    await con.execute(f'INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?, ?);', values)
                    await con.commit()
        print('Successfully updated messages in database.')

    @update.before_loop
    async def wait_until_ready(self):
        await self.bot.wait_until_ready()
    
def setup(bot):
    bot.add_cog(Widbase(bot))
