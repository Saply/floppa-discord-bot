import datetime as dt

from discord.errors import NotFound
from discord import Button, ButtonStyle, Interaction
from discord.commands import ApplicationContext
from discord.ui import View, button

from utils.schemas import ClassCollection


 
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
        await self.confirmation_message.delete_original_response() 
        await interaction.response.send_message(f"<@{self.ctx.author.id}> **{self.class_tbd.class_details.class_name} [{self.class_tbd.class_details.class_group}]** has been successfully deleted!")


    @button(label = "No! I don't want that!", style = ButtonStyle.danger, emoji = "✖")
    async def no_button_callback(self, button: Button, interaction: Interaction):
        await self.confirmation_message.delete_original_response() 
        await interaction.response.send_message(f"<@{self.ctx.author.id}> Class removal cancelled")
        

    async def on_timeout(self):
        try:
            await self.confirmation_message.delete_original_response()
            await self.ctx.respond(f"<@{self.ctx.author.id}> Too slow, class deletion cancelled.")

        # The "timeout" timer still persists even after the user has already clicked a button. Currently, I don't know if Pycord has a way to
        # cancel that timeout, so the only option was to catch the error that is raised whenever I try to delete a message that was already deleted
        except NotFound:
            return 


# Sorting classes in list
class ClassSort:
    def __init__(self, class_list: list, sort_by: str):
        self.class_list = class_list

        # lol
        if sort_by == "time":
            self._timeSort()
        elif sort_by == "alphabet":
            self._alphabetSort()
        elif sort_by == "class_id":
            self._idSort()

    def _alphabetSort(self):
        self.class_list = sorted(self.class_list, key = lambda letter: letter[1])

    def _timeSort(self):
        EPOCH_FIRST_CLASS = 345300
        EPOCH_WEEK = 604800

        # Do % by a week in epoch time to account for classes that won't be in the same week (eg. 14-3-2022 and 21-3-2022)
        for item in self.class_list:
            item[3] = item[3] % EPOCH_WEEK 
        # Using first class in a week (Monday 8:00AM) as comparison, add additional values to epoch times which are smaller than it to avoid broken sorting
            if item[3] < EPOCH_FIRST_CLASS:
                item[3] = item[3] + EPOCH_WEEK

        self.class_list = sorted(self.class_list, key = lambda x: x[3])

    def _idSort(self):
        self.class_list = sorted(self.class_list, key = lambda id: id[4])

    def listGetter(self, order: bool):
        if order == True:
            return self.class_list
        else:
            return self.class_list[::-1]


class MiscellaneousCommands:
    @staticmethod
    def next_date(weekday: int, time: str) -> dt.datetime:
        today = dt.datetime.now()
        time = time.replace(" ", "")

        result = today + dt.timedelta(days = (weekday - today.weekday()) % 7)

        # Insert time into result 
        result = dt.datetime.strptime(f"{dt.datetime.strftime(result, '%d-%m-%Y')} {time}", "%d-%m-%Y %I:%M%p") - dt.timedelta(minutes = 5)
        
        # Compares if result is less than current time, if it is, add one week to it
        if today < result:
            return result 
        else: 
            return result + dt.timedelta(days = 7)


    

    
