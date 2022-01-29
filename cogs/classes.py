import discord, random, os, asyncio, mongoengine as mdb, datetime as dt
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice

from data.schemas import ClassCollection, ClassDetails


class Classes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    # aaaa https://discord-py-slash-command.readthedocs.io/en/components/discord_slash.client.html?highlight=subcommand#discord_slash.client.SlashCommand.subcommand
    # option types https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    @cog_ext.cog_subcommand(
        base = "class",
        name = "add",
        description = "Add classes with these wide variety of options!!!",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "repeatable",
                description = "Is the class repeated weekly or not?",
                option_type = 4,
                required = True,
                choices = [
                    create_choice(
                        name = "Yes",
                        value = 1
                    ),
                    create_choice(
                        name = "No",
                        value = 0
                    )
                ]
            ),
            create_option(
                name = "class_title",
                description = "What is the name and class code of the class? (eg. PCT0101 INTRO TO COMPUTING TECH)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "link",
                description = "Enter the URL of the class",
                option_type = 3,
                required = True 
            ),
            create_option(
                name = "lecturer_name",
                description = "What is the name of the lecturer?",
                option_type = 3,
                required = True 
            ),
            create_option(
                name = "group",
                description = "Enter the lecture/tutorial group (eg. TT1V, TT8L, TC2V)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "duration",
                description = "Enter the duration of the class in minutes (eg. 60, 120, 1440)",
                option_type = 4,
                required = True
            ),
            create_option(
                name = "date",
                description = "Enter the date of the class in DD-MM-YYYY format (eg. 12-12-2022, 01-04-2022)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "start_time",
                description = "Enter the time for when the class begins (eg. 9:00 AM, 12:30 PM, 4:00 PM)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "channel",
                description = "Tag the name of the channel you want the bot to post reminders in (eg. #fci, #fist, #general)",
                option_type = 3,
                required = True
            )
        ]
    )
    
    async def class_add(self, ctx: SlashContext, repeatable: int, class_title: str, link: str, lecturer_name: str, group: str, duration: int, date: str, start_time: str, channel: str):
        
        # This is scuffed but trust me it works (it even accepts 9:00        AM)
        try:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M %p")
        except ValueError:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M%p")
        
        add = ClassCollection(
                channel_id = channel[2:-1],
                repeatable = bool(repeatable),
                dates = date_and_time,

                class_details = ClassDetails(
                    class_name = class_title, 
                    class_group = group,
                    duration = duration, 
                    

                    link = link,
                    lecturer_name = lecturer_name      
                )
            )
            
        add.save()
        
        await ctx.send(f"Class successfully registered!")

    # Add multiple optional parameters except class ID
    # test optional parameters
    @cog_ext.cog_subcommand(
        base = "class",
        name = "edit",
        description = "Update details of a class using the class ID",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "class_id",
                description = "The ID of the class you want to edit/update",
                option_type = 4,
                required = True
            )  
        ]
    )
    async def class_edit(self, ctx: SlashContext, class_id: int):
        await ctx.send(class_id)


    @cog_ext.cog_subcommand(
        base = "class",
        name = "remove",
        description = "Remove classes using their ID",
        guild_ids = [536835061895397386]
    )
    async def class_remove(self, ctx: SlashContext):
        await ctx.send("remove")
    

    @cog_ext.cog_subcommand(
        base = "class",
        name = "check",
        description = "Check classes using the ID that is assigned to them",
        guild_ids = [536835061895397386]
    )
    async def class_check(self, ctx: SlashContext):   
        await ctx.send("awooga")


    @cog_ext.cog_subcommand(
        base = "class",
        name = "list",
        description = "Check the list of all currently active classes",
        guild_ids = [536835061895397386]
    )
    async def class_list(self, ctx: SlashContext):
        await ctx.send("list")
    

    # I really wanted t
    @cog_ext.cog_subcommand(
        base = "class",
        name = "subscribe",
        description = "Choose which class you want to be pinged for",
        guild_ids = [536835061895397386]
    )
    async def class_subscribe(self, ctx: SlashContext):
        await ctx.send("subscribe")

    @cog_ext.cog_subcommand(
        base = "class",
        name = "unsubscribe",
        description = "Unchoose which class you want to be pinged for (i'll make a better description eventually)",
        guild_ids = [536835061895397386]
    )
    async def class_unsubscribe(self, ctx: SlashContext):
        await ctx.send("unsubscribe")
    
    
def setup(client: commands.Bot):
    client.add_cog(Classes(client))