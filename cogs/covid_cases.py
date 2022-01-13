from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import discord, pandas as pd

class CovidCases(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name = "covid", description = "what")
    async def covidcases(self, ctx: SlashContext):
        
        await "a"

def setup(client):
    client.add_cog(CovidCases(client))