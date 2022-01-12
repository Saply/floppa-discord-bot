import discord, random, os, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

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
    
    @cog_ext.cog_slash(name="test",
             description="This is just a test command, nothing more.",
             guild_ids = [536835061895397386],
             options=[
               create_option(
                 name="optone",
                 description="This is the first option we have.",
                 option_type=3,
                 required=False,
                 choices=[
                  create_choice(
                    name="ChoiceOne",
                    value="DOGE!"
                  ),
                  create_choice(
                    name="ChoiceTwo",
                    value="NO DOGE"
                  )
                ]
               )
             ])
    async def test(self, ctx: SlashContext, optone: str):
        await ctx.send(content=f"Wow, you actually chose {optone}? :(")

    @commands.command(name = "echo", description = "lol idk", guild_ids = [536835061895397386])
    async def tttttttt(self, ctx: SlashContext):
        await ctx.message.delete()
        
        embed = discord.Embed(title = "what want to send", description = "this will expire after like 30 seconds lol")
        sent = await ctx.send(embed = embed)

        """
        def check(message)
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


def setup(client: commands.Bot):
    client.add_cog(Test(client))