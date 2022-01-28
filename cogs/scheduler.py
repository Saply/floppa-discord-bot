# probably merge this with other relevant files or just put anything that requires tasks.loops inside this file
import discord, datetime as dt
from discord.ext import commands, tasks 
from data.schemas import *

class Scheduler(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.clock.start()
    
    # query db every 30 minutes to check if a class is happening or not 
    # i set it to 1 for now since i need to test things
    @tasks.loop(minutes = 1)
    async def clock(self):
        # I had to remove the microseconds and seconds because including smaller units messes up every single query
        current_time = dt.datetime.now().replace(microsecond = 0, second = 0)
        
        classes_query = ClassCollection.objects.filter(dates = current_time)
        # If there are no classes, return
        if not classes_query:
            print(f"No class now, back to sleep. Time: {current_time}")
            return
        
        # For loop is used in case there are multiple classes with the same time
        for classes in classes_query:
            embed = discord.Embed(title = "**Class Link**", url = classes.class_details.link, description = f"""```yaml {classes.class_details.link}```""")
            embed.set_author(name = "Class is starting!", url = classes.class_details.link, icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
            embed.set_thumbnail(url = "https://mindamind.files.wordpress.com/2010/10/mmu.jpg")
            embed.add_field(name = "ID", value = classes.id, inline = True)
            embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
            embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
            embed.add_field(name = "Lecture/Lab Group\t", value = classes.class_details.class_group, inline = True)
            embed.add_field(name = "Lecturer/Lab Tutor", value = classes.class_details.lecturer_name, inline = True)
            embed.set_footer(text = "Use the /class command to check out the options to add/update/remove/check classes")
            
            # Gets channel to post class in from database
            # the issue is over here
            discord_channel = self.client.get_channel(classes.channel_id)
            await discord_channel.send(embed = embed)
            
            # (i'll work on this eventually)
            # Checks if the class is repeated or not
            # If it is repeated, update/replace the date with the same time but in 7 days 
            if classes.repeatable == True:
                print("man this class is repeatable thats cool")
            # If it is not repeated, delete the record from the database
            else:
                print("nice")


    # This is essential to ensure the bot doesnt kill itself before startup
    @clock.before_loop
    async def before(self):
        await self.client.wait_until_ready()


def setup(client: commands.Bot):
    client.add_cog(Scheduler(client))
