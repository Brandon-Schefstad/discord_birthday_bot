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
    guild_id = os.getenv("GUILD_ID_LEET")
    channel_id = os.getenv("CHANNEL_ID_LEET")

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # self.check.start()
        pass

    @commands.command()
    async def set_birthday(self, ctx):
        (text, author) = self.get_text_and_author(ctx, inspect.stack()[0][3])
        birthday_match = re.search(r"([0-9]+(-[0-9]+)+)", text)
        birthday_dict = self.read_csv()
        # If author of message already in csv.
        if not birthday_match:
            await ctx.send(f"Incorrect formatting, please try again with MM-DD-YYYY.")
        elif author in birthday_dict:
            await ctx.send(
                f"You've already set your birthday! It's {birthday_dict[author]}. If you need to override, type `!change_birthday` with the new birthday as MM-DD-YYYY."
            )
        else:
            self.write_csv(author, text)
            await ctx.send(
                f"Hello {author}! Your birthday has been set to {text.lstrip()}. "
            )

    @tasks.loop(hours=12)
    async def check(self):
      ctx = self.bot.guilds[1]
      birthday_dict = self.read_csv()
      for person in birthday_dict:
          if birthday_dict[person][:5] == str(date.today().strftime("%m-%d")):
              age = self.get_age(birthday_dict[person])
              member = discord.utils.find(lambda m: m.name == person, ctx.members)
              await ctx.get_channel(self.channel_id).send(
                  f'@everyone'
              )
              await ctx.get_channel(self.channel_id).send(
                f"Today is <@{member.id}>'s {age} birthday. Be sure to send them some love! <3"
              )
      await self.bot.close()

    def read_csv(self):
        with open("tmp/bdays.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            birthday_dict = {}
            for bday in reader:
                birthday_dict[bday[0]] = bday[1].strip()
            return birthday_dict

    def write_csv(self, author, text):
        with open("tmp/bdays.csv", "a", newline="") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow([author, text])

    def get_text_and_author(self, ctx, command_name):
        text = ctx.message.content.split(command_name)[1]
        author = ctx.message.author.name
        return (text, author)

    def get_age(self, birthday: str, today=date.today()):
        """
        calculates ordinal ages from birthdays, assuming birthday has already
        passed
        `get_age("12-02-2000")` returns `"24th"` when run in 2024
        """
        birthday = datetime.strptime(birthday, "%m-%d-%Y")
        age = today.year - birthday.year
        return "".join(
            [
                str(age),
                (
                    ["th", "st", "nd", "rd", "th"][min(age % 10, 4)]
                    if not 11 <= (age % 100) <= 13
                    else "th"
                ),
            ]
        )


async def setup(bot):
    await bot.add_cog(birthday_cog(bot))
