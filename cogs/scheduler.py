import datetime as dt

from discord import Embed, Cog, Bot
from discord.ext import tasks 

from utils.schemas import ClassCollection

class Scheduler(Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.class_clock.start()

    # query db every x minutes to check if a class is happening or not 
    @tasks.loop(minutes = 1)
    async def class_clock(self):
        current_time = dt.datetime.now().replace(microsecond = 0, second = 0)
        
        classes_query = ClassCollection.objects.filter(date_time = current_time)
        # If there are no classes, return
        if not classes_query:
            print(f"No class now, back to sleep. Time: {current_time}")
            return
        
        # For loop is used in case there are multiple classes with the same time
        for classes in classes_query:
            temp_date = classes.date_time + dt.timedelta(minutes = 5)
            embed = Embed(title = "** ** **>>> __CLASS LINK__ <<<**", url = classes.class_details.link, description = f"```yaml\n{classes.class_details.link}```")
            embed.set_author(name = f"Class is starting!", icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
            embed.set_thumbnail(url = self.client.get_guild(classes.guild_id).icon)
            embed.add_field(name = "Class ID", value = f"**{classes.class_id}**", inline = False)
            embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
            embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
            embed.add_field(name = "Group", value = classes.class_details.class_group, inline = True)
            embed.add_field(name = "Lecturer/Tutor", value = classes.class_details.lecturer_name, inline = True)
            embed.add_field(name = "Time", value = temp_date.strftime("%A %I:%M %p"), inline = True)
            embed.add_field(name = "Channel", value = f"<#{classes.channel_id}>", inline = True)
            embed.set_footer(text = "Use the /class command to check out other options to add/update/remove/check classes")  
            
            notifications = ' '.join(f"<@{str(id)}>" for id in classes.notify)
            # Gets channel to post class in from database
            discord_channel = self.client.get_channel(classes.channel_id)
            await discord_channel.send(content = notifications, embed = embed)

            
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
        

def setup(client: Bot):
    client.add_cog(Scheduler(client))
