import os

from discord.ext import commands
from discord import Status, Game

from mongoengine import connect
from dotenv import load_dotenv


# Token client stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

connect("db-classes")
client = commands.Bot(command_prefix = '!')

# Called when the bot is ready to be used
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def status():
    await client.wait_until_ready()
    await client.change_presence(status = Status.online, activity = Game(name = "If something here doesn't work then you know who to blame")) 

client.loop.create_task(status())


if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
