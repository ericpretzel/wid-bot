import config
import discord
from discord.ext import commands
import youtube_dl
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
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = list()

    audio_group = discord.SlashCommandGroup('radio', 'Audio-related commands', [config.GUILD_ID])

    @audio_group.command(description='Play audio from the given YouTube URL.')
    async def play(self, ctx: discord.ApplicationContext, url: str, channel: discord.VoiceChannel = None):
        # if no channel specified, assume it's the one that the user is connected to
        if channel is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
            else:
                return await ctx.respond('Please specify a channel to connect to or be connected to a channel already.', ephemeral=True)

        client = await channel.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
        
        await ctx.respond(f'**Now playing:** {player.title}')


    @audio_group.command(description='Stop playing music.')
    async def stop(self, ctx: discord.ApplicationContext):
        await ctx.voice_client.disconnect()
        await ctx.respond('Disconnected from voice.', ephemeral=True)

def setup(bot):
    bot.add_cog(Audio(bot))
