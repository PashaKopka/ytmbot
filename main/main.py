import os
import time

import discord
import youtube_dl
from discord.ext import commands
import pathlib
import urllib.request
import re
import urllib.parse

from ytmbot.main.settings import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix='!')

FILE_PATH = pathlib.Path(__file__).parent.absolute()
MP3_FILE_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'usenetrc': True,
    'outtmpl': os.path.normpath(FILE_PATH.__str__() + '/audio/%(title)s.%(ext)s'),
}


def download_music_file(url: str) -> str:
    with youtube_dl.YoutubeDL(MP3_FILE_OPTIONS) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        filename = f'{FILE_PATH}\\audio\{info_dict.get("title", None)}.webm'
        ydl.download([url])

    return filename


def search(search_keyword):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_keyword)
    html = urllib.request.urlopen(url)
    start = time.time()
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    stop = time.time()
    print(f'search: {stop - start}')
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return url


def prepare_search_keywords(words):
    search_keywords = '+'
    search_keywords = search_keywords.join(words)
    search_keywords = search_keywords.encode('utf-8').decode('utf-8')
    return search_keywords


@client.command()
async def play(ctx, *args, channel: discord.VoiceChannel = None):
    destination = channel if channel else ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_state.voice.move_to(destination)
        return

    await destination.connect()

    if args[0][:32] == 'https://www.youtube.com/watch?v=':
        file = download_music_file(args[0])
    else:
        search_keywords = prepare_search_keywords(args)
        url = search(search_keywords)
        file = download_music_file(url)

    file = file.replace('/', '_')

    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    audio_source = discord.FFmpegPCMAudio(file)
    voice_client.play(audio_source, after=None)


client.run(DISCORD_BOT_TOKEN)
