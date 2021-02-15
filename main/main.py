import discord
from discord.ext import commands

from ytmbot.main.settings import DISCORD_BOT_TOKEN

client = commands.Bot(command_prefix='!')


@client.command()
async def hello(context, argument):
    await context.send(argument)


client.run(DISCORD_BOT_TOKEN)
