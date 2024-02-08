from discord.ext import commands
import discord
import re
import csv

def write_csv(author, text):
    with open('bdays.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([author, text])

def read_csv():
    with open('bdays.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)  
        birthday_dict = {}
        for bday in reader:
            birthday_dict[bday[0]] = bday[1]
        return birthday_dict


@commands.command(name="test")
async def test(ctx):
    await ctx.send("working!")

@commands.command(name="change_birthday")
async def change_birthday(ctx,new_birthday):
    birthday_dict = read_csv()
    if str(ctx.author) in birthday_dict:
        author_birthday = birthday_dict[str(ctx.author)]
        await ctx.send(f"Girl, youve already set your birthday! It's {author_birthday}. If you need to override, type !change_birthday with the new birthday as XX-XX-XXXX.")
    else:
        write_csv(ctx.author, new_birthday)
        await ctx.send(f'Hello {ctx.author}! Your birthday has been set to {new_birthday}. ')


@commands.command(name="get_birthday")
async def get_birthday(ctx):
    birthday_dict = read_csv()

    if str(ctx.author) in birthday_dict:
        author_birthday = birthday_dict[str(ctx.author)]
        await ctx.message.channel.send(
            f"{ctx.author}, your birthday is on {author_birthday}."
        )
    else:
        await ctx.send("Not Found!")



