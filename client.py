import os, datetime as dt, discord
from mongoengine import connect
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext


from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, create_select, create_select_option
from discord_slash.model import ButtonStyle
# https://pypi.org/project/discord-py-slash-command/

# token client stuff
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# connect to da database
connect("db-classes")

# bot stuff
client = commands.Bot(command_prefix = '!')
slash = SlashCommand(client, sync_commands = True)


# Called when the bot is ready to be used
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def status():
    await client.wait_until_ready()
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name = "If something here doesn't work then you know who to blame"))
    return 

client.loop.create_task(status())


# use waybackmachine to read docs (wtf)
# https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html


if __name__ == '__main__':
    # get everything in the cogs folder, the . represents folder path like cogs/cogfile.py. Have to load it without the .py extension at the end so thats what the [:-3] does
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
