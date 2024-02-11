import discord
from discord.ext import commands, tasks
import asyncio
import os
import re
import csv
import discord
from datetime import date


class info_cog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        print("Starting up Info cog!")

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.command()
    async def scan(self, ctx):
        room = ctx.guild
        print(
            f"""
        Name of server: {room}
        Server ID: {room.id}
        Current channel: {ctx.channel}
        Current number of members: {room.member_count}
        Member List: {room.members.__dict__}
        Available channels:{room.text_channels}
        Message from: {ctx.message.author}
        Author ID: {ctx.message.author.id}
        """
        )


async def setup(bot):
    await bot.add_cog(info_cog(bot))