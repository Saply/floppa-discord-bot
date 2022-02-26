import random, os

from discord import File, Embed
from discord.ext import commands
from discord.commands import slash_command, ApplicationContext, Option, OptionChoice



class Animal(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 


    @slash_command(
        name = "post_animal",
        description = "Posts a random animal image of your choice",
        guild_ids = [871300534999584778, 536835061895397386],
    ) 
    async def post_animal(self, ctx: ApplicationContext, 
        animal: Option(str, "The animal you want to pick", 
            choices = [
                OptionChoice(
                    name = "Caracal",
                    value = "caracal"
                ),
                OptionChoice(
                    name = "Capybara",
                    value = "capybara"
                ),
                OptionChoice(
                    name = "Shiba Inu",
                    value = "shiba-inu"
                )
            ]   
        )
    ):
        # Getting path to file
        OptionChoice
        img_list = os.listdir(f"./images/{animal}")
        img_string = random.choice(img_list)
        path = f"./images/{animal}/{img_string}"

        # This is extremely important
        compliments = ["cute", "funny", "hilarious", "extravagant", "cat"]

        # Making the embed
        embed = Embed(title = f"A random {animal}", description = random.choice(compliments), color = 0x3240a8)
        image_file = File(path, filename = "image.jpg")
        embed.set_image(url = "attachment://image.jpg")
        await ctx.respond(file = image_file, embed = embed)
        
    

def setup(client: commands.Bot):
    client.add_cog(Animal(client))
    