import json, datetime as dt

from discord import Embed, HTTPException, TextChannel, Bot, Cog
from discord.commands import ApplicationContext, SlashCommandGroup, Option, OptionChoice


from utils.schemas import ClassCollection, ClassDetails
from utils.custom_discord_classes import ClassConfirmDeletionView, ClassSort, MiscellaneousCommands

class Classes(Cog):
    def __init__(self, client: Bot):
        self.client = client
        
    class_sub = SlashCommandGroup("class", "List of class subcommands", guild_ids = [536835061895397386, 981068613769371718])


    @class_sub.command(
        name = "add",
        description = "Add classes with these wide variety of options!!",
    )
    async def class_add(self, ctx: ApplicationContext, 
        repeatable: Option(int, "Is the class repeated weekly or not?", required = True,
            choices = [
                OptionChoice(
                    name = "Yes",
                    value = 1
                ),
                OptionChoice(
                    name = "No",
                    value = 0
                )
            ]
        ),
        class_name: Option(str, "What is the name and class code of the class? (eg. PCT0101 INTRO TO COMPUTING TECH)", required = True),
        link: Option(str, "Enter the URL of the class", required = True),
        lecturer_name: Option(str, "What is the name of the lecturer?", required = True),
        group: Option(str, "Enter the lecture/tutorial group (eg. TT1V, TT8L, TC2V)", required = True),
        duration: Option(int, "Enter the duration of the class in minutes (eg. 60, 120, 1440)", required = True),
        day: Option(int, "What day is the class on?", required = True,
            choices = [
                OptionChoice(
                    name = "Monday",
                    value = 0
                ),
                OptionChoice(
                    name = "Tuesday",
                    value = 1
                ),
                OptionChoice(
                    name = "Wednesday",
                    value = 2
                ),
                OptionChoice(
                    name = "Thursday",
                    value = 3
                ),
                OptionChoice(
                    name = "Friday",
                    value = 4
                ),
                OptionChoice(
                    name = "Saturday",
                    value = 5
                ),
                OptionChoice(
                    name = "Sunday",
                    value = 6
                )
            ]
        ),
        start_time: Option(str, "Enter the time for when the class begins (eg. 9:00 AM, 12:30 PM, 4:00PM)", required = True),
        channel: Option(TextChannel, "Tag the channel you want the bot to post reminders in (eg. #fci, #fist, #general)", required = True)
    ):
        try:          
            add = ClassCollection(
                    channel_id = channel.id,
                    guild_id = ctx.guild_id,
                    repeatable = bool(repeatable),
                    date_time = MiscellaneousCommands.next_date(day, start_time),

                    class_details = ClassDetails(
                        class_name = class_name, 
                        class_group = group,
                        duration = duration, 
                        
                        link = link,
                        lecturer_name = lecturer_name      
                    )
                )
                
            add.save()

            await ctx.respond(f"Class successfully added for **{add.class_details.class_name} [{add.class_details.class_group}]**!\n**Class ID: __{add.class_id}__**")

        except Exception as error:
            await ctx.respond(f"**Error when adding class:** {error}")


    @class_sub.command(
        name = "edit",
        description = "Update details of a class using the class ID"
    )
    async def class_edit(self, ctx: ApplicationContext,
        class_id: Option(int, "The ID of the class you want to edit details of", required = True),
        class_name: Option(str, "What is the name and class code of the class? (eg. PCT0101 INTRO TO COMPUTING TECH)", required = False, default = None),
        link: Option(str, "Enter the URL of the class", required = False, default = None),
        lecturer_name: Option(str, "What is the name of the lecturer?", required = False, default = None),
        group: Option(str, "Enter the lecture/tutorial group (eg. TT1V, TT8L, TC2V)", required = False, default = None),
        duration: Option(int, "Enter the duration of the class in minutes (eg. 60, 120, 1440)", required = False, default = None),
        date_and_time: Option(str, "Enter the date of the class in DD-MM-YYYY format and time (eg. 12-12-2022 9:03 AM)", required = False, default = None),
        channel: Option(TextChannel, "Tag the channel you want the bot to post classes in (eg. #fci, #fist, #general)", required = False, default = None)
    ):
        # Query result of class_id integer
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()

        if not classes or ctx.guild_id != classes.guild_id:
            await ctx.respond(f"No such class ID exists for **{ctx.guild}**!")
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

        await ctx.respond("Class successfully edited!")
   

    @class_sub.command(
        name = "remove",
        description = "Remove classes using their class ID"
    )
    async def class_remove(self, ctx: ApplicationContext,
        class_id: Option(int, "The ID of the class you want to delete", required = True)
    ):
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        if not classes or ctx.guild_id != classes.guild_id:
            await ctx.respond(f"No such class ID exists for **{ctx.guild}**!")
            return
        
        temp_date: dt.datetime = classes.date_time + dt.timedelta(minutes = 5)
        embed = Embed(title = "Class Details", description = f"```yaml\n{classes.class_details.link}```", color = 0xdb161d)
        embed.set_thumbnail(url = self.client.get_guild(classes.guild_id).icon)
        embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
        embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
        embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
        embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
        embed.add_field(name = "Time", value = temp_date.strftime("%A %I:%M %p"), inline = True)
        embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)


        view = ClassConfirmDeletionView(timeout = 8, ctx = ctx, class_tbd = classes)
        confirmation = await ctx.respond("Are you sure you want to delete this class?", view = view, embed = embed)
        view.confirmation_message = confirmation
        

    @class_sub.command(name = "check", description = "Check class details using the ID that is assigned to them")
    async def class_check(self, ctx: ApplicationContext, 
        class_id: Option(int, "The class ID of the class you want to edit details of", required = True)
    ): 
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        if not classes or ctx.guild_id != classes.guild_id:
            await ctx.respond(f"No such class ID exists for **{ctx.guild}**!")
            return

        temp_date: dt.datetime = classes.date_time + dt.timedelta(minutes = 5)
        embed = Embed(title = "** ** **>>> __CLASS LINK__ <<<**", url = classes.class_details.link, description = f"```yaml\n{classes.class_details.link}```", color = 0x9e30d1)
        embed.set_author(name = f"Class Details", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
        embed.set_thumbnail(url = self.client.get_guild(classes.guild_id).icon)
        embed.add_field(name = "Class ID", value = f"**{classes.class_id}**", inline = False)
        embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
        embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
        embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
        embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
        embed.add_field(name = "Time", value = temp_date.strftime("%A %I:%M %p"), inline = True)
        embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)
        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")  
        await ctx.respond(embed = embed)

    
    @class_sub.command(name = "list", description = "Check the list of all currently active classes")
    async def class_list(self, ctx: ApplicationContext,
        sort_by: Option(str, "What do you want to sort the list by?", required = False, default = "class_id",
            choices = [
                OptionChoice(
                    name = "Class ID",
                    value = "class_id"
                ),
                OptionChoice(
                    name = "Alphabet",
                    value = "alphabet"
                ),
                OptionChoice(
                    name = "Time",
                    value = "time"
                )
            ]
        ),
        order: Option(int, "Do you want to display the list in reversed order?", required = False, default = 1,
            choices = [
                OptionChoice(
                    name = "Yes",
                    value = 0
                ),
                OptionChoice(
                    name = "No",
                    value = 1
                )
            ]
        )
    ):
        class_list = []

        for classes in ClassCollection.objects.filter(guild_id = ctx.guild_id):
            # Index 3 and 4 in class_list is reserved for sorting
            class_list.append( 
                [
                    f"**{classes.class_id}**",
                    f"{classes.class_details.class_name} **[{classes.class_details.class_group}]**",
                    (classes.date_time + dt.timedelta(minutes = 5)).strftime("%A %I:%M %p"),
                    dt.datetime.timestamp(classes.date_time),
                    classes.class_id
                ]
            )
        
        class_list = ClassSort(class_list, sort_by).listGetter(bool(order))

        embed = Embed(description = f"Use `/class check` to check details of each class", color = 0x3aded6)
        embed.set_author(name = f"List of All Active Classes", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")

        embed.add_field(name = "Class ID", value = "\n".join(i[0] for i in class_list), inline = True)
        embed.add_field(name = "Subject Name (Group)", value = "\n".join(j[1] for j in class_list), inline = True)
        embed.add_field(name = "Time", value = "\n".join(k[2] for k in class_list), inline = True)


        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")

        try:
            await ctx.respond(embed = embed)
        except HTTPException:
            await ctx.respond(f"No active classes found for **{ctx.guild}**!") 

    
    @class_sub.command(name = "subscribe", description = "Choose which class you want to be pinged for")
    async def class_subscribe(self, ctx: ApplicationContext, 
        class_id: Option(int, "The ID of the class you wish to be pinged for", required = True)
    ):
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        
        if not classes or ctx.guild_id != classes.guild_id:
            await ctx.respond(f"No such class ID exists for **{ctx.guild}**!")
            return
        
        classes.update(add_to_set__notify = ctx.author.id, upsert = True)
        await ctx.respond(f"<@{ctx.author.id}> You have been subscribed to receive notifications for **{classes.class_details.class_name} [{classes.class_details.class_group}]**")

    
    @class_sub.command(name = "subscribemany", description = "Subscribe to many classes at once")
    async def subscribe_many(self, ctx: ApplicationContext, 
        class_ids: Option(str, "List down multiple class IDs separated by space (eg. /class subscribemany class_ids: 1 3 5 7 10)", required = True)
    ):
        class_ids_list: list = [int(i) for i in class_ids.split()]
        
        successful_subscriptions = []
        unsuccessful_subscriptions = []
        for class_id in class_ids_list:
            classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()

            if not classes or ctx.guild_id != classes.guild_id:
                unsuccessful_subscriptions.append(f"**{class_id}**, ")
            else:
                classes.update(add_to_set__notify = ctx.author.id, upsert = True)
                successful_subscriptions.append(f"**{classes.class_details.class_name} [{classes.class_details.class_group}]**, ")
        
        content = f"You have been subscribed to receive notifications for: {' '.join(successful_subscriptions)[:-2] if successful_subscriptions else '**-**'}\nThe following class IDs do not exist:  {' '.join(unsuccessful_subscriptions)[:-2] if unsuccessful_subscriptions else '**-**'}"

        await ctx.respond(f"<@{ctx.author.id}> {content}")


    @class_sub.command(name = "subscribelist", description = "Check the list of which classes you wish to be notified for")
    async def class_subscribelist(self, ctx: ApplicationContext,
        sort_by: Option(str, "What do you want to sort the list by?", required = False, default = "class_id",
            choices = [
                OptionChoice(
                    name = "Class ID",
                    value = "class_id"
                ),
                OptionChoice(
                    name = "Alphabet",
                    value = "alphabet"
                ),
                OptionChoice(
                    name = "Time",
                    value = "time"
                )
            ]
        ),
        order: Option(int, "Do you want to display the list in reversed order?", required = False, default = 1,
            choices = [
                OptionChoice(
                    name = "Yes",
                    value = 0
                ),
                OptionChoice(
                    name = "No",
                    value = 1
                )
            ]
        )
    ):  
        class_list = []

        for classes in ClassCollection.objects.filter(notify__in = [ctx.author.id]):
            if not classes:
                await ctx.respond(f"You are currently not subscribed to any classes <@{ctx.author.id}>")
                return
            
            class_list.append( 
                [
                    f"**{classes.class_id}**",
                    f"{classes.class_details.class_name} **[{classes.class_details.class_group}]**",
                    (classes.date_time + dt.timedelta(minutes = 5)).strftime("%A %I:%M %p"),
                    dt.datetime.timestamp(classes.date_time),
                    classes.class_id
                ]
            )
        
        class_list = ClassSort(class_list, sort_by).listGetter(bool(order))
        
        embed = Embed(description = f"Use `/class check` to check details of each class", color = 0x3aded6)
        embed.set_author(name = f"List of Classes {str(ctx.author)[:-5]} is subscribed to", icon_url = ctx.author.avatar)


        embed.add_field(name = "Class ID", value = "\n".join(i[0] for i in class_list), inline = True)
        embed.add_field(name = "Subject Name (Group)", value = "\n".join(j[1] for j in class_list), inline = True)
        embed.add_field(name = "Time", value = "\n".join(k[2] for k in class_list), inline = True)

        embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")

        await ctx.respond(f"<@{ctx.author.id}>", embed = embed)


    @class_sub.command(name = "unsubscribe", description = "Choose which class you don't want to be pinged for anymore")
    async def class_unsub(self, ctx: ApplicationContext, 
        class_id: Option(int, "The ID of the class you don't want to be notified for", required = True)
    ):
        classes: ClassCollection = ClassCollection.objects.filter(class_id = class_id).first()
        
        if not classes or ctx.guild_id != classes.guild_id:
            await ctx.respond(f"No such class ID exists for **{ctx.guild}**!")
            return
        
        classes.update(pull__notify = ctx.author.id, upsert = True)
        await ctx.respond(f"<@{ctx.author.id}> You have been unsubscribed from receiving notifications for **{classes.class_details.class_name} [{classes.class_details.class_group}]**")



    
def setup(client: Bot):
    client.add_cog(Classes(client))