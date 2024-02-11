import discord
from discord.ext import commands, tasks
import asyncio
import os
import re
import csv
import discord
from datetime import date
import inspect


class birthday_cog(commands.Cog):
    guild_id = 712797901096747059
    channel_id = 712797901549731862
    def __init__(self, bot) -> None:
        self.bot = bot
        print(self.guild_id)

    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()
#         await self.bot.get_guild(self.guild_id).get_channel(
#             self.channel_id
#         ).send(
#             f"""Hey everyone! I am your birthday bot. I accept the following commands:

# `!set_birthday` followed by your birthdate in MM-DD-YYYY format. 
# `!change_birthday` for if you make a typo.

# We can always add in more commands as we see fit :) 

# This bot is not always online as that would be very expensive! I'll run it locally for a few days so people can set their birthdays. But if you miss that window just dm me and I can add you. After the few days it'll just wake up once a day to see if any of the dates from the csv match. 
#             """
#         )

    @commands.command()
    async def set_birthday(self, ctx):
        print(ctx.guild.id)
        (text, author) = self.get_text_and_author(ctx, inspect.stack()[0][3])
        birthday_match = re.search(r"([0-9]+(-[0-9]+)+)", text)
        birthday_dict = self.read_csv()
        if author in birthday_dict:
            await ctx.send(
                f"Girl, youve already set your birthday! It's {birthday_dict[author]}. If you need to override, type `!change_birthday` with the new birthday as MM-DD-YYYY."
            )
        else:
            self.write_csv(author, text)
            await ctx.send(f"Hello {author}! Your birthday has been set to {text}. ")

    @tasks.loop(hours=12)
    async def check(self):
        ctx = self.bot.get_guild(self.guild_id)
        birthday_dict = self.read_csv()
        for person in birthday_dict:
            if birthday_dict[person][:5] == str(date.today().strftime("%m-%d")):
                member = discord.utils.find(lambda m: m.name == person, ctx.members)
                await ctx.get_channel(self.channel_id).send(
                    f'@everyone'
                )
                await ctx.get_channel(self.channel_id).send(
                    f"Today is <@{member.id}>'s birthday. Be sure to send them some love! "
                )

    @commands.command()
    async def change_birthday(self, ctx):
        (text, author) = self.get_text_and_author(ctx, "change_birthday")
        self.write_csv(author, text)
        await ctx.send(f"Your birthday has been updated to {text.lstrip()}")

    def read_csv(self):
        with open("tmp/bdays.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            birthday_dict = {}
            for bday in reader:
                birthday_dict[bday[0]] = bday[1].strip()
            return birthday_dict

    def write_csv(self, author, text):
        with open("tmp/bdays.csv", "w", newline="") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow([author, text])

    def get_text_and_author(self, ctx, command_name):
        text = ctx.message.content.split(command_name)[1]
        author = ctx.message.author.name
        return (text, author)


async def setup(bot):
    await bot.add_cog(birthday_cog(bot))
