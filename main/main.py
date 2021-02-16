import os
import time

import discord
import youtube_dl
from discord.ext import commands
import pathlib

from ytmbot.main.settings import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix='!')

FILE_PATH = pathlib.Path(__file__).parent.absolute()
MP3_FILE_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'usenetrc': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.normpath(FILE_PATH.__str__() + '/audio/%(title)s.%(ext)s'),
}


def download_music_file(url: str) -> str:
    with youtube_dl.YoutubeDL(MP3_FILE_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        filename = f'{FILE_PATH}\\audio\{info_dict.get("title", None)}.mp3'
        ydl.download([url])

    return filename


@client.command()
async def play(ctx, *args, channel: discord.VoiceChannel = None):
    destination = channel if channel else ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_state.voice.move_to(destination)
        return

    await destination.connect()

    file = download_music_file('https://www.youtube.com/watch?v=AMCwYdTJ_PE&ab_channel=Future-Topic')

    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    audio_source = discord.FFmpegPCMAudio(file)
    voice_client.play(audio_source, after=None)


client.run(DISCORD_BOT_TOKEN)
