import discord, random, os, asyncio

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from data.schemas import ClassDetails, ClassCollection
class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(
        name = "hello",
        description = "Sends a message of choice",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "option",
                description = "choose your word",
                required = True,
                option_type = 3,
                choices = [
                    create_choice(
                        name = "World",
                        value = "world!!"
                    ),
                    create_choice(
                        name = "You",
                        value = "you!!"
                    )
                ]
            )
        ]
    )
    async def _hello(self, ctx: SlashContext, option: str):
        await ctx.send(option)

    @commands.command(name = "echo", description = "lol idk", guild_ids = [536835061895397386])
    async def tttttttt(self, ctx: SlashContext):
        await ctx.message.delete()
        embed = discord.Embed(title = "what want to send", description = "this will expire after like 30 seconds lol")
        sent = await ctx.send(embed = embed)
        """
        lambda function is equivalent to def check(message):
        """

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 60,
                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
            )
            if msg:
                await sent.delete()
                await msg.delete()
                await ctx.send(msg.content)

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelled due to timeout zamn youre slow af", delete_after = 5)

    
    @cog_ext.cog_slash(name='cooltest', description = "yea", guild_ids = [536835061895397386])
    async def addition(self, ctx: SlashContext):
        for classes in ClassCollection.objects().filter(id = 3):
            embed = discord.Embed(title = "**Class Link**", url = classes.class_details.link, description = f"```{classes.class_details.link}```")
            embed.set_author(name = "**Class is starting!**", url = classes.class_details.link, icon_url = "https://cdn.discordapp.com/emojis/872501924925165598.webp?size=128&quality=lossless")
            embed.set_thumbnail(url = "https://mindamind.files.wordpress.com/2010/10/mmu.jpg")
            embed.add_field(name = "ID", value = classes.id, inline = True)
            embed.add_field(name = "Duration", value = f"{classes.class_details.duration} minutes", inline = True)
            embed.add_field(name = "Class Name", value = classes.class_details.class_name, inline = True)
            embed.add_field(name = "Lecture/Lab Group\t", value = classes.class_details.class_group, inline = True)
            embed.add_field(name = "Lecturer/Lab Tutor", value = classes.class_details.lecturer_name, inline = True)
            embed.set_footer(text = "Use the /class command to check out the options to add/update/remove/check classes")
        await ctx.send(embed = embed)
    
    @cog_ext.cog_subcommand(base="group", name="say", description = "yea", guild_ids = [536835061895397386])
    async def group_say(self, ctx: SlashContext, clsname: str):
        print(f"Da channel ID is {clsname} dawgg")
        await ctx.send(f"Da channel ID is {clsname} dawgg")

def setup(client: commands.Bot):
    client.add_cog(Test(client))