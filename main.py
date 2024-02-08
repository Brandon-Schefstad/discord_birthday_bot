from discord.ext import commands
import os
# bot.py
import asyncio
import os
import re

import discord
from dotenv import load_dotenv

load_dotenv()

client =  discord.Client(intents=discord.Intents.default())

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client.run("token")