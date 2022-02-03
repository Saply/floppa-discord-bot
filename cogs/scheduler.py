# probably merge this with other relevant files or just put anything that requires tasks.loops inside this file
import discord, datetime as dt
from discord.ext import commands, tasks 
from data.schemas import *

class Scheduler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.class_clock.start()
    
    # query db every 30 minutes to check if a class is happening or not 
    # i set it to 1 for now since i need to test things
    @tasks.loop(minutes = 1)
    async def class_clock(self):
        # I had to remove the microseconds and seconds because including smaller units messes up the queries
        current_time = dt.datetime.now().replace(microsecond = 0, second = 0)
        
        classes_query = ClassCollection.objects.filter(date_time = current_time)
        # If there are no classes, return
        if not classes_query:
            print(f"No class now, back to sleep. Time: {current_time}")
            return
        
        # For loop is used in case there are multiple classes with the same time
        for classes in classes_query:
            embed = discord.Embed(title = "**Class Link**", url = classes.class_details.link, description = f"```yaml\n{classes.class_details.link}```")
            embed.set_author(name = "Class is starting!", url = classes.class_details.link, icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/871307003111276544/936935102301220934/image_2022-01-29_184417.png")
            embed.add_field(name = "Class ID", value = classes.class_id, inline = True)
            embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
            embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
            embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
            embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
            embed.set_footer(text = "Use the /class command to check out the options to add/update/remove/check classes")
            
            # Gets channel to post class in from database
            discord_channel = self.client.get_channel(classes.channel_id)
            await discord_channel.send(embed = embed)
            
            # Checks if the class is repeated or not
            # If it is repeated, update the date with the same time but for next week
            if classes.repeatable:
                classes.update(set__date_time = classes.date_time + dt.timedelta(days = 7))
            # If it is not repeated, delete the record from the database 
            else:
                classes.delete()


    # This is essential to ensure the bot doesnt kill itself before startup
    @class_clock.before_loop
    async def before(self):
        await self.client.wait_until_ready()


def setup(client: commands.Bot):
    client.add_cog(Scheduler(client))
