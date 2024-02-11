# bot.py
import asyncio
import os
import re
import csv
import discord
from dotenv import load_dotenv
from discord.ext import commands
from cogs.birthday_cog import birthday_cog
from cogs.info_cog import info_cog


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    print("This bot is running!")


async def startcogs():
    await bot.load_extension("cogs.birthday_cog")
    await bot.load_extension("cogs.info_cog")


asyncio.run(startcogs())
bot.run(TOKEN)
