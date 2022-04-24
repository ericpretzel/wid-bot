import config
import discord
from discord.ext import commands, pages, tasks
import youtube_dl
from youtubesearchpython import VideosSearch
import asyncio

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # Bind to ipv4 since ipv6 addresses cause issues at certain times
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {"options": "-vn"}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, youtube_url, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")
        self.youtube_url = youtube_url
        self.requester = "Nobody"

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), youtube_url=url, data=data)

class Audio(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.song_queue: list[YTDLSource] = list()
        self.current_song: YTDLSource = None

    audio_group = discord.SlashCommandGroup('radio', 'Audio-related commands', [config.GUILD_ID])

    @tasks.loop(minutes=5, count=None)
    async def refresh_ytdl_task(self):
        print('refreshing ytdls')
        """
        Refreshes the urls for songs in queue because they get invalidated after a certain amount of time.
        """
        new_queue: list[YTDLSource] = list()
        for song in self.song_queue:
            new_song = await YTDLSource.from_url(song.youtube_url, loop=self.bot.loop)
            new_song.requester = song.requester
            new_queue.append(new_song)
            await asyncio.sleep(1)
        self.song_queue = new_queue
            
    @audio_group.command(description='Play audio from the given YouTube URL or search query.')
    async def play(self, ctx: discord.ApplicationContext, video: discord.Option(str, "YouTube URL or search query"), channel: discord.Option(discord.VoiceChannel, "The channel to connect to", required=False)):
        """
        Adds music to queue.
        Starts playing music if it isn't playing already.
        """
        # if no channel specified, assume it's the one that the user is connected to
        if channel is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                return await ctx.respond('Please specify a channel to connect to or be connected to a channel already.', ephemeral=True)
        await ctx.defer()

        client = ctx.voice_client or await channel.connect()

        if video.startswith('http'):
            url = video
        else:
            url = VideosSearch(video, limit=1).result()['result'][0]['link']
            print("url:", url)

        song = await YTDLSource.from_url(url, loop=self.bot.loop)
        song.requester = ctx.author.display_name
        song.youtube_url = url
        self.song_queue.append(song)
        self.play_music(client)

        if not self.refresh_ytdl_task.is_running():
            self.refresh_ytdl_task.start()

        await ctx.respond(f'Added to queue: **{song.title}**')

    @audio_group.command(description="Vote to skip the current song.")
    async def skip(self, ctx: discord.ApplicationContext):
        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.respond("You're not in the correct voice channel!", ephemeral=True)
        await ctx.defer()
        await ctx.respond("skipped lol")
        ctx.voice_client.pause()

        # manually refresh just in case
        await self.refresh_ytdl_task()
        self.play_music(ctx.voice_client)

    def play_music(self, client: discord.VoiceClient):
        """
        Helper function for `play` and `skip`.
        Starts playing songs from queue.
        """
        if len(self.song_queue) == 0 and not client.is_playing():
            return self.refresh_ytdl_task.stop()
        elif client.is_playing():
            return
        self.current_song = self.song_queue.pop(0)
        client.play(self.current_song, after=lambda e: self.play_music(client) if not e else print(f'Player error: {e}'))

    @audio_group.command(description='Stop playing music.')
    async def stop(self, ctx: discord.ApplicationContext):
        if ctx.voice_client:
            self.refresh_ytdl_task.stop()
            await ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.respond('Disconnected from voice.')
        else:
            await ctx.respond('Not connected to a voice channel!', ephemeral=True)

    @audio_group.command(description='View the current song queue.')
    async def queue(self, ctx: discord.ApplicationContext):
        # not playing music and no songs in queue
        if not ctx.voice_client or (ctx.voice_client and not ctx.voice_client.is_playing()):
            return await ctx.respond("Nothing is playing.", ephemeral=True)
        # no songs in queue, but playing music
        elif len(self.song_queue) == 0:
            embed = discord.Embed(
                title="**There are no songs in queue**"
            )
            embed.add_field(name=f"**Currently playing:** {self.current_song.title}", value= f"[Added by {self.current_song.requester}]({self.current_song.youtube_url})", inline=False)
            paginator = pages.Paginator(pages=[embed])
            return await paginator.respond(ctx.interaction)

        paginator_pages = list()
        for i in range(0, len(self.song_queue), 5):
            embed = discord.Embed(title='**Song queue**')
            embed.add_field(name=f"**Currently playing:** {self.current_song.title}", value= f"[Added by {self.current_song.requester}]({self.current_song.youtube_url})", inline=False)
            for j, song in enumerate(self.song_queue[i:i+5]):
                embed.add_field(name=f"{j+i+1}. **{song.title}**", value=f"[Added by {song.requester}]({song.youtube_url})", inline=False)
            paginator_pages.append(embed)
        paginator = pages.Paginator(pages=paginator_pages)
        await paginator.respond(ctx.interaction)

def setup(bot):
    bot.add_cog(Audio(bot))
