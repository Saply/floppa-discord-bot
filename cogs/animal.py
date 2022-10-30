import requests

from discord import Embed, SlashCommandGroup, Bot, Cog
from discord.commands import ApplicationContext, Option, OptionChoice

class Animal(Cog):
    def __init__(self, client: Bot):
        self.client = client 

    animal_sub = SlashCommandGroup("animal", "List of animal subcommands", guild_ids = [536835061895397386, 981068613769371718])


    @animal_sub.command(
        name = "post",
        description = "Posts a random animal image of your choice",
    ) 
    async def post_animal(self, ctx: ApplicationContext, 
        animal: Option(str, "The animal you want to pick", 
            choices = [
                OptionChoice(
                    name = "Cat",
                    value = "cat"
                ),
                OptionChoice(
                    name = "Shiba Inu",
                    value = "shiba"
                ),
                OptionChoice(
                    name = "Capybara",
                    value = "capy"
                )
            ]   
        )
    ):
        if animal == "capy":
            img = requests.get("https://api.capybara-api.xyz/v1/image/random").json()['image_urls']['large']
            fact = requests.get("https://api.capybara-api.xyz/v1/facts/random").json()['fact']
            footer = "Fact and image provided by The Capybara API"
        elif animal == "cat":
            img = requests.get("https://shibe.online/api/cats?count=1").json()[0]
            fact = requests.get("https://catfact.ninja/fact?max_length=140").json()['fact']
            footer = "Fact provided by Cat Facts API and image provided by Shibe Online Cats API"
        else:
            img = requests.get("http://shibe.online/api/shibes?count=1").json()[0]
            fact = requests.get("https://dog-api.kinduff.com/api/facts?number=1").json()['facts'][0]
            footer = "Fact provided by kinduff's Dog API and image provided by Shibe Online Shiba Inu API"

        # Making the embed
        embed = Embed(title = f"A random {animal}", description = fact, color = 0x3240a8)
        embed.set_image(url = img)
        embed.set_footer(text = footer)
        await ctx.respond(embed = embed)


def setup(client: Bot):
    client.add_cog(Animal(client))
    