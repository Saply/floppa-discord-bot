import json
import discord, random, os, mongoengine as mdb, datetime as dt
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
        guild_ids = [536835061895397386, 871300534999584778],
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
    
    # i'll add validation eventually
    async def class_add(self, ctx: SlashContext, repeatable: int, class_name: str, link: str, lecturer_name: str, group: str, duration: int, date: str, start_time: str, channel: discord.channel.TextChannel):
        # This is scuffed but trust me it works
        try:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M %p")
        except ValueError:
            date_and_time = dt.datetime.strptime(f"{date} {start_time}", "%d-%m-%Y %I:%M%p")
        
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

    
    # For updating classes
    @cog_ext.cog_subcommand(
        base = "class",
        name = "edit",
        description = "Update details of a class using the class ID",
        guild_ids = [536835061895397386, 871300534999584778],
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
            )
        ]
    )
    # TODO: Do the same for changing channels and datetime as well
    async def class_edit(self, ctx: SlashContext, class_id: int, class_name: str = None, link: str = None, 
                         lecturer_name: str = None, group: str = None, duration: int = None):
        args = {
            'class_name': class_name,
            'class_group': group,
            'duration': duration,
            'link': link,
            'lecturer_name': lecturer_name
        }

        # Query result of class_id integer
        classes = ClassCollection.objects.filter(class_id = class_id).first()
        query = json.loads(classes.to_json())
        new_date_time = query['date_time']
        new_channel = query['channel_id']
        new_class_details = query['class_details']
        
        ### FOR CLASS DETAILS
        # Replaces values in query with values in args (if applicable)
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
        guild_ids = [536835061895397386]
    )
    async def class_remove(self, ctx: SlashContext):
        
        await ctx.send("remove")
    

    @cog_ext.cog_subcommand(
        base = "class",
        name = "check",
        description = "Check class details using the ID that is assigned to them",
        guild_ids = [536835061895397386, 871300534999584778],
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
        classes = ClassCollection.objects.filter(class_id = class_id).first()

        embed = discord.Embed(title = "**Class Link**", url = classes.class_details.link, description = f"```yaml\n{classes.class_details.link}```")
        embed.set_author(name = f"Class Details", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/871307003111276544/936935102301220934/image_2022-01-29_184417.png")
        embed.add_field(name = "Class ID", value = classes.class_id, inline = False)
        embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
        embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
        embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
        embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
        embed.add_field(name = "Time", value = classes.date_time.strftime("%A %I:%M %p"), inline = True)
        embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)
        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")  
        await ctx.send(embed = embed)


    @cog_ext.cog_subcommand(
        base = "class",
        name = "list",
        description = "Check the list of all currently active classes",
        guild_ids = [536835061895397386, 871300534999584778]
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
        
        
        # include class ID, class name and also group
        embed = discord.Embed(description = f"**Lorem ipsum dolor sir amet**")
        embed.set_author(name = f"List of All Active Classes", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")


        embed.add_field(name = "Class ID", value = class_ids, inline = True)
        embed.add_field(name = "Class", value = class_names, inline = True)
        embed.add_field(name = "Group", value = class_groups, inline = True)

        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")

        await ctx.send(embed = embed)
    

    # like and subscribe !!
    @cog_ext.cog_subcommand(
        base = "class",
        name = "subscribe",
        description = "Choose which class you want to be pinged for",
        guild_ids = [536835061895397386]
    )
    async def class_subscribe(self, ctx: SlashContext):
        print(ctx.author_id)
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