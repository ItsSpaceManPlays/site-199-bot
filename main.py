import discord
from discord.ext import commands

def run():
    intents = discord.Intents.all()

    bot = commands.Bot(command_prefix="/", intents=intents)