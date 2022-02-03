from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import discord, pandas as pd

class CovidCases(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "covid", description = "what", guild_ids = [536835061895397386])
    async def covidcases(self, ctx: SlashContext):
        await ctx.send(ctx.author_id)

def setup(client):
    client.add_cog(CovidCases(client))