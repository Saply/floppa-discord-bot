from discord.ext import commands
from discord_slash import SlashContext
# use validation = function() argument
class CustomError(Exception):
    """Base class for other exceptions"""
    pass 

class Test(CustomError):
    pass 

# ignore for now 
class DiscordUtility(commands.Cog):
    def rolesGetter(self, ctx: SlashContext) -> list:
        return [1, 2, 3]

# raise CustomError
try:
    raise Test("oh no our table")
except CustomError:
    print("oh no")
