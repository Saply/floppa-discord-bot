import os, discord, datetime
import pandas as pd
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

# token client stuff
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = '!!')
slash = SlashCommand(client, sync_commands = True)


@client.event
# Called when the bot is ready to be used
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # await client.change_presence(game = discord.Game(name = "ooga booga"))
   
# done using callbacks
@client.event
async def on_message(message):
    if message.author == client.user:   # If the author of the message is the bot, return
        return


if __name__ == '__main__':
    # get everything in the cogs folder, the . represents folder path like cogs/bennett.py. Have to load it without the .py extension at the end so thats what the [:-3] does
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
