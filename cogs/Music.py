import asyncio
import discord
from discord.ext import commands
import youtube_dl
from discord import app_commands, Interaction

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join", description="Join the voice channel")
    async def join(self, interaction: Interaction, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        if interaction.guild.voice_client is not None:
            return await interaction.guild.voice_client.move_to(channel)
        
        interaction.response.send_message(f"Joined {channel}")
        await channel.connect()
    
    @app_commands.command(name="play", description="Play a song")
    async def play(self, interaction: Interaction, *, query: str):
        """Plays a file from the local filesystem"""
        
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        interaction.guild.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.response.send_message(f'Now playing: {query}')

    @app_commands.command(name="yt", description="Plays a song from an url")
    async def yt(self, interaction: Interaction, *, url: str):
        """Plays from a url (almost anything youtube_dl supports)"""
        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.response.send_message(f'Now playing: {player.title}')

    @app_commands.command(name="stream", description="Streams from an url (better option)")
    async def stream(self, interaction: Interaction, *, url: str):
        """Streams from a url (same as yt, but doesn't predownload)"""
        async with interaction.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.response.send_message(f'Now playing: {player.title}')

    @app_commands.command(name="volume", description="Change the player's volume")
    async def volume(self, interaction: Interaction, volume: int):
        """Changes the player's volume"""
        if interaction.guild.voice_client is None:
            return await interaction.response.send_message("Not connected to a voice channel.")

        interaction.guild.voice_client.source.volume = volume / 100
        await interaction.response.send_message(f"Changed volume to {volume}%")

    @app_commands.command(name="stop", description="Stops and disconnects the bot from voice")
    async def stop(self, interaction: Interaction):
        """Stops and disconnects the bot from voice"""

        await interaction.guild.voice_client.disconnect()


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
