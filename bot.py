# bot.py
import asyncio
import os
import re
import csv
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client =  discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.content and message.author!=client.user :
        print(str(client.user.id) in message.content)
        text = message.content.split(f'{client.user.id}> ')[1]
        birthday_match = re.search(r"([0-9]+(-[0-9]+)+)", text)
        author = message.author.name
        if '!change_birthday' in text:
          new_birthday = text.split(' ')[1]
          write_csv(author, new_birthday)
        elif birthday_match:
            birthday_dict = read_csv(message)
            channel = message.channel
            if author in birthday_dict:
                await channel.send(f"Girl, youve already set your birthday! It's {birthday_dict[author]}. If you need to override, type !change_birthday with the new birthday as XX-XX-XXXX.")
            else:    
              write_csv(author, text)
              await channel.send(f'Hello {message.author}! Your birthday has been set to {text}. ')
        elif text[0] == '$':
          birthday_dict = read_csv(message)
          await message.channel.send(
            f"{author}, your birthday is {birthday_dict[author]}."
        )

def read_csv(message):
    with open('bdays.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        birthday_dict={}
        for bday in reader:
            birthday_dict[bday[0]] = bday[1]
        return birthday_dict
    
def write_csv(author, text):
    with open('bdays.csv', 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=' ',
                              quotechar='|', quoting=csv.QUOTE_MINIMAL)
      writer.writerow([author , text])
client.run(TOKEN)
