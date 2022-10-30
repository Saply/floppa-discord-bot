import os

from discord import Status, Game, Intents, Bot
from mongoengine import connect
from dotenv import load_dotenv


# .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_USERNAME = os.getenv('mongo-username')
MONGO_PASSWORD = os.getenv('mongo-password')
MONGO_DB_NAME = os.getenv('mongo-db-name')

connect(db = MONGO_DB_NAME, username = MONGO_USERNAME, password = MONGO_PASSWORD, host = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.wsfli.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority")

client = Bot(command_prefix = '!', intents = Intents.all())


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
