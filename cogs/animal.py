import discord, random, os, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Animal(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 
    
    @cog_ext.cog_slash(
        name = "post_animal",
        description = "Posts a random animal image of your choice",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "animal",
                description = "Pick an animal!",
                option_type = 3,
                required = True,
                choices = [
                    create_choice(
                        name = "Caracal",
                        value = "caracal"
                    ),
                    create_choice(
                        name = "Capybara",
                        value = "capybara"
                    ),
                    create_choice(
                        name = "Shiba Inu",
                        value = "shiba-inu"
                    )
                ]
            )
        ]
    )
    async def post_animal(self, ctx: SlashContext, animal: str):
        # Getting path to file
        img_list = os.listdir(f"./images/{animal}")
        img_string = random.choice(img_list)
        path = f"./images/{animal}/{img_string}"

        # Making the embed
        embed = discord.Embed(title = f"A random {animal}", description = random.choice(["cute", "funny", "hilarious"]), color = 0x3240a8)
        image_file = discord.File(path, filename = "image.jpg")
        embed.set_image(url = "attachment://image.jpg")
        await ctx.send(file = image_file, embed = embed)
        
    

def setup(client: commands.Bot):
    client.add_cog(Animal(client))
    