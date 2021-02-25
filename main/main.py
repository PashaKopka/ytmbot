import discord

from discord.ext import commands

from ytmbot.main.music_downloader import download_music_file, prepare_search_keywords, search
from ytmbot.main.settings import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix='!')


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
