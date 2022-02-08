import json, asyncio, datetime as dt

import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component

from data.schemas import ClassCollection, ClassDetails


class Classes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    @cog_ext.cog_subcommand(
        base = "class",
        name = "add",
        description = "Add classes with these wide variety of options!!!",
        guild_ids = [871300534999584778, 536835061895397386],
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
                name = "class_name",
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
                description = "Enter the date of the class in DD-MM-YYYY format (eg. 12-12-2022, 25-4-2022)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "start_time",
                description = "Enter the time for when the class begins (eg. 9:00 AM, 12:30 PM, 4:00PM)",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "channel",
                description = "Tag the channel you want the bot to post reminders in (eg. #fci, #fist, #general)",
                option_type = 7,
                required = True
            )
        ]
    )
    async def class_add(self, ctx: SlashContext, repeatable: int, class_name: str, link: str, lecturer_name: str, 
                        group: str, duration: int, date: str, start_time: str, channel: discord.channel.TextChannel):
        # This is scuffed but trust me it works
        try:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M %p")
        except ValueError:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M%p")
        
        date_and_time = date_and_time - dt.timedelta(minutes = 5)

        add = ClassCollection(
                channel_id = channel.id,
                repeatable = bool(repeatable),
                date_time = date_and_time,

                class_details = ClassDetails(
                    class_name = class_name, 
                    class_group = group,
                    duration = duration, 
                    
                    link = link,
                    lecturer_name = lecturer_name      
                )
            )
            
        add.save()

        await ctx.send(f"Class successfully added for **{add.class_details.class_name} [{add.class_details.class_group}]**!\n**Class ID: __{add.class_id}__**")

    
    @cog_ext.cog_subcommand(
        base = "class",
        name = "edit",
        description = "Update details of a class using the class ID",
        guild_ids = [871300534999584778, 536835061895397386],
        options = [
            # Required parameter
            create_option(
                name = "class_id",
                description = "The ID of the class you want to edit details of",
                option_type = 4,
                required = True
            ),
            # Optional parameters
            create_option(
                name = "class_name",
                description = "What is the name and class code of the class? (eg. PCT0101 INTRO TO COMPUTING TECH)",
                option_type = 3,
                required = False
            ),
            create_option(
                name = "link",
                description = "Enter the URL of the class",
                option_type = 3,
                required = False 
            ),
            create_option(
                name = "lecturer_name",
                description = "What is the name of the lecturer?",
                option_type = 3,
                required = False 
            ),
            create_option(
                name = "group",
                description = "Enter the lecture/tutorial group (eg. TT1V, TT8L, TC2V)",
                option_type = 3,
                required = False
            ),
            create_option(
                name = "duration",
                description = "Enter the duration of the class in minutes (eg. 60, 120, 1440)",
                option_type = 4,
                required = False
            ),
            create_option(
                name = "date_and_time",
                description = "Enter the date of the class in DD-MM-YYYY format and time (eg. 12-12-2022 9:03 AM)",
                option_type = 3,
                required = False
            ),
            create_option(
                name = "channel",
                description = "Tag the channel you want the bot to post reminders in (eg. #fci, #fist, #general)",
                option_type = 7,
                required = False
            )
        ]
    )
    async def class_edit(self, ctx: SlashContext, class_id: int, class_name: str = None, link: str = None, lecturer_name: str = None, 
                         group: str = None, duration: int = None, date_and_time: str = None, channel: discord.channel.TextChannel = None):
        # Query result of class_id integer
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()

        if not classes:
            await ctx.send("No such class ID exists!")
            return

        query = json.loads(classes.to_json())
        
        ### For date and time 
        current_date_time = classes.date_time  

        if date_and_time is not None:
            try:
                new_date_time = dt.datetime.strptime(date_and_time, "%d-%m-%Y %I:%M %p")
            except ValueError:
                new_date_time = dt.datetime.strptime(date_and_time, "%d-%m-%Y %I:%M%p")

            if (current_date_time != date_and_time) and (date_and_time is not None):
                new_date_time -= dt.timedelta(minutes = 5)
                classes.update(set__date_time = new_date_time)
        

        ### For channel
        current_channel = classes.channel_id 
        if (current_channel != channel) and (channel is not None):
            classes.update(set__channel_id = channel.id)
        

        ### For class details
        args = {
            'class_name': class_name,
            'class_group': group,
            'duration': duration,
            'link': link,
            'lecturer_name': lecturer_name
        }

        new_class_details = query['class_details']

        for key in args: 
            if (new_class_details[key] != args[key]) and (args[key] is not None):
                new_class_details[key] = args[key]

        classes.update(set__class_details = new_class_details)

        
        classes.save()

        await ctx.send("Class successfully edited!")
    

    @cog_ext.cog_subcommand(
        base = "class",
        name = "remove",
        description = "Remove classes using their ID",
        guild_ids = [871300534999584778, 536835061895397386],
        options = [
            create_option(
                name = "class_id",
                description = "The ID of the class you want to delete",
                option_type = 4,
                required = True
            )
        ]
    )
    async def class_remove(self, ctx: SlashContext, class_id: int):
        # Create embed
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        if not classes:
            await ctx.send("No such class ID exists!")
            return
        
        temp_date: dt.datetime = classes.date_time + dt.timedelta(minutes = 5)
        embed = discord.Embed(title = "Class Details", description = f"```yaml\n{classes.class_details.link}```", color = 0xdb161d)
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/871307003111276544/936935102301220934/image_2022-01-29_184417.png")
        embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
        embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
        embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
        embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
        embed.add_field(name = "Time", value = temp_date.strftime("%A %I:%M %p"), inline = True)
        embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)


        # Button component
        buttons = [
            create_button(style = ButtonStyle.green, label = "Yes, I want to delete this class", custom_id = "yes"),
            create_button(style = ButtonStyle.danger, label = "No! I don't want that! Not for another 10 years at least!", custom_id = "no"),
            create_button(style = ButtonStyle.gray, label = "Cancel", custom_id = "cancel")
        ]
        action_row = create_actionrow(*buttons)

        confirmation = await ctx.send("Are you sure you want to delete this class?", embed = embed, components=[action_row])
        
        try:
            button_ctx: ComponentContext = await wait_for_component(self.client, components = action_row, timeout = 8)


            if button_ctx.custom_id == "yes":
                classes.delete()
                await ctx.send("Class successfully removed!")
            elif button_ctx.custom_id == "no":
                await ctx.send(f"Class removal cancelled <@{ctx.author_id}>")
            else:
                await ctx.send(f"seems like you cancelled it idiot <@{ctx.author_id}>")

            await confirmation.delete()
        

        except asyncio.TimeoutError:
            await confirmation.delete()
            await ctx.send("Class removal process timed out, damn you're slow as hell fr")
       
    

    @cog_ext.cog_subcommand(
        base = "class",
        name = "check",
        description = "Check class details using the ID that is assigned to them",
        guild_ids = [871300534999584778, 536835061895397386],
        options = [
            create_option(
                name = "class_id",
                description = "The ID of the class you want to edit details of",
                option_type = 4,
                required = True
            )
        ]
    )
    async def class_check(self, ctx: SlashContext, class_id: int): 
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        if not classes:
            await ctx.send("No such class ID exists!")
            return

        temp_date: dt.datetime = classes.date_time + dt.timedelta(minutes = 5)
        embed = discord.Embed(title = "** ** **>>> __CLASS LINK__ <<<**", url = classes.class_details.link, description = f"```yaml\n{classes.class_details.link}```", color = 0x9e30d1)
        embed.set_author(name = f"Class Details", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/871307003111276544/936935102301220934/image_2022-01-29_184417.png")
        embed.add_field(name = "Class ID", value = f"**{classes.class_id}**", inline = False)
        embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
        embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
        embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
        embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
        embed.add_field(name = "Time", value = temp_date.strftime("%A %I:%M %p"), inline = True)
        embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)
        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")  
        await ctx.send(embed = embed)


    @cog_ext.cog_subcommand(
        base = "class",
        name = "list",
        description = "Check the list of all currently active classes",
        guild_ids = [871300534999584778, 536835061895397386]
    )
    async def class_list(self, ctx: SlashContext):
        class_ids = ""
        class_names = ""
        class_groups = ""

        count = 0
        for classes in ClassCollection.objects:
            class_ids += f"{classes.class_id}\n" if count % 2 == 0 else f"**{classes.class_id}**\n"
            class_names += f"{classes.class_details.class_name}\n" if count % 2 == 0 else f"**{classes.class_details.class_name}**\n"
            class_groups += f"{classes.class_details.class_group}\n" if count % 2 == 0 else f"**{classes.class_details.class_group}**\n"

            count += 1
        
        
        embed = discord.Embed(description = f"Use `/class check` to check details of each class", color = 0x3aded6)
        embed.set_author(name = f"List of All Active Classes", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")


        embed.add_field(name = "Class ID", value = class_ids, inline = True)
        embed.add_field(name = "Class", value = class_names, inline = True)
        embed.add_field(name = "Group", value = class_groups, inline = True)

        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")

        await ctx.send(embed = embed)
    

    # Notify
    @cog_ext.cog_subcommand(
        base = "class",
        name = "subscribe",
        description = "Choose which class you want to be pinged for",
        guild_ids = [871300534999584778, 536835061895397386],
        options = [
            create_option(
                name = "class_id",
                description = "The ID of the class you want to be pinged for",
                option_type = 4,
                required = True
            )
        ]
    )
    async def class_subscribe(self, ctx: SlashContext, class_id: int):
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        classes.update(add_to_set__notify = ctx.author_id, upsert = True)
        await ctx.send(f"<@{ctx.author_id}> You have been subscribed to receive notifications for **{classes.class_details.class_name} [{classes.class_details.class_group}]**")


    @cog_ext.cog_subcommand(
        base = "class",
        name = "unsubscribe",
        description = "Choose which class you don't want to be pinged for anymore",
        guild_ids = [536835061895397386, 871300534999584778],
        options = [
            create_option(
                name = "class_id",
                description = "The ID of the class you don't want to be notified for",
                option_type = 4,
                required = True
            )
        ]
    )
    async def class_unsub(self, ctx: SlashContext, class_id: int):
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        classes.update(pull__notify = ctx.author_id, upsert = True)
        await ctx.send(f"<@{ctx.author_id}> You have been unsubscribed from receiving notifications for **{classes.class_details.class_name} [{classes.class_details.class_group}]**")
    
    
    
def setup(client: commands.Bot):
    client.add_cog(Classes(client))