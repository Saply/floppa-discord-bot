import datetime as dt
from discord.ext.pages import *

from typing import Awaitable, List, Union
from discord.errors import NotFound
from discord import Button, ButtonStyle, File, Embed, SlashCommandGroup, InputTextStyle, Interaction
from discord.ext import commands
from discord.commands import slash_command, ApplicationContext, Option, OptionChoice
from discord.ui import Modal, InputText, View, button

from utils.schemas import ClassCollection, ClassDetails


 
# Confirm deletion of a class
class ClassConfirmDeletionView(View):
    def __init__(self, timeout: int, ctx: ApplicationContext, class_tbd: ClassCollection):
        super().__init__(timeout = timeout)
        self.ctx = ctx
        self.class_tbd = class_tbd
        self.confirmation_message: Interaction

        
    @button(label = "Yes, I want to delete this class", style = ButtonStyle.green, emoji = "✔")
    async def yes_button_callback(self, button: Button, interaction: Interaction):
        self.class_tbd.delete()
        await self.confirmation_message.delete_original_message() 
        await interaction.response.send_message(f"<@{self.ctx.author.id}> **{self.class_tbd.class_details.class_name} [{self.class_tbd.class_details.class_group}]** has been successfully deleted!")


    @button(label = "No! I don't want that!", style = ButtonStyle.danger, emoji = "✖")
    async def no_button_callback(self, button: Button, interaction: Interaction):
        await self.confirmation_message.delete_original_message() 
        await interaction.response.send_message(f"<@{self.ctx.author.id}> Class removal cancelled")
        

    async def on_timeout(self):
        try:
            await self.confirmation_message.delete_original_message()
            await self.ctx.respond(f"<@{self.ctx.author.id}> Too slow, class deletion cancelled.")

        # The "timeout" timer still persists even after the user has already clicked a button. Currently, I don't know if Pycord has a way to
        # cancel that timeout, so the only option was to catch the error that is raised whenever I try to delete a message that was already deleted
        except NotFound:
            return


class AnimalSubmissionModal(Modal):
    pass 

# Creating multiple page embeds
class CustomPaginator(Paginator):
    def __init__(self, all_pages: List[Embed]):
        super().__init__()

    # one page = 15 classes perhaps 
    # for loop to generate multiple embeds 
    # also use ClassCollection.count() 



    