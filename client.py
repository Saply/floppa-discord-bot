import os, datetime as dt
from mongoengine import connect
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission

# token client stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# connect to da database
connect("db-classes")

# bot stuff
client = commands.Bot(command_prefix = '!')
slash = SlashCommand(client, sync_commands = True)

# done using callbacks
@client.event
# Called when the bot is ready to be used
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html


if __name__ == '__main__':
    # get everything in the cogs folder, the . represents folder path like cogs/cogfile.py. Have to load it without the .py extension at the end so thats what the [:-3] does
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
