import random, os

from discord import File, Embed, SlashCommandGroup, InputTextStyle, Interaction
from discord.ext import commands
from discord.commands import ApplicationContext, Option, OptionChoice
from discord.ui import Modal, InputText

class Animal(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 

    animal_sub = SlashCommandGroup("animal", "List of animal subcommands", guild_ids = [536835061895397386, 871300534999584778, 497567524800561153])

    @animal_sub.command(
        name = "post",
        description = "Posts a random animal image of your choice",
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
        
    @animal_sub.command(
        name = "submit",
        description = "Submit an animal image to the bot (requires image URL)"
    )
    async def submit_animal_img(self, ctx: ApplicationContext):
        # subclass modal soon
        
        modal = Modal(title = "You're not supposed to see this yet")
        modal.add_item(InputText(style = InputTextStyle.singleline, label = "If you see this pop-up", placeholder = "then it's not finished yet", value = None, required = False))
        modal.add_item(InputText(style = InputTextStyle.singleline, label = "Feel free to mess around though", placeholder = "since there's nothing here yet", value = None, required = False))

        
        async def modal_callback(interaction: Interaction):
            print(modal.children[0].value) 
            print(modal.children[1].value)
            await interaction.response.send_message(f"heehee")

        
        
        modal.callback = modal_callback
        # keep this
        await ctx.interaction.response.send_modal(modal)

def setup(client: commands.Bot):
    client.add_cog(Animal(client))
    