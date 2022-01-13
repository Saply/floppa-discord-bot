import discord, random, os, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice

class Classes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    # aaaa https://discord-py-slash-command.readthedocs.io/en/components/discord_slash.client.html?highlight=subcommand#discord_slash.client.SlashCommand.subcommand
    # option types https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    @cog_ext.cog_subcommand(
        base = "class",
        name = "add",
        description = "Add classes with these wide variety of options!!!",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "test",
                description = "honestly idk",
                option_type = 3,
                required = True,
                choices = [
                    create_choice(
                        name = "cat",
                        value = "cat"
                    ),
                    create_choice(
                        name = "dog",
                        value = "dog"
                    )
                ]
            ),
            create_option(
                name = "lol_eee",
                description = "idk either",
                option_type = 3,
                required = True
            ),
            create_option(
                name = "repeatable",
                description = "mann is it repeatable or not",
                option_type = 5,
                required = True

                # turns out option type 5 doesn't require you to make a choice array
                # choices = [
                #     create_choice(
                #         name = "ye la",
                #         value = True
                #     ),
                #     create_choice(
                #         name = "no la",
                #         value = False
                #     )
                # ]
            )
        ]
    )
    async def class_add(self, ctx: SlashContext, test: str, lol_eee: str, repeatable: bool):
        await ctx.send(f"{test} and {lol_eee} repeatable or not {repeatable}")

    @cog_ext.cog_subcommand(
        base = "class",
        name = "remove",
        description = "Add classes with these wide variety of options!!!",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "test",
                description = "honestly idk",
                option_type = 3,
                required = True,
                choices = [
                    create_choice(
                        name = "cat",
                        value = "cat"
                    ),
                    create_choice(
                        name = "dog",
                        value = "dog"
                    )
                ]
            )
        ]
    )
    async def class_remove(self, ctx: SlashContext, test: str, class_title: str, link: str, name: str, group: str, duration: int, start_time: str):
        await ctx.send(f"{class_title}\n{link}\n{name}\n{group}\n{duration}\n{start_time} and the class repeatability is {test}")
"""
    @cog_ext.cog_subcommand(
        base = "class",
        name = "remove",
        description = "Add classes with these wide variety of options!!!",
        guild_ids = [536835061895397386],
        options = [
            create_option(
                name = "Repeatable",
                description = "Is the class repeated weekly or does it occur only once?",
                required = True,
                option_type = 5,
                choices = [
                    create_choice(
                        name = "True",
                        value = True
                    ),
                    create_choice(
                        name = "False",
                        value = False
                    )
                ]
            )
        ]
    )
    async def class_remove(self, ctx: SlashContext, class_title: str, link: str, name: str, group: str, duration: int, start_time: str, Repeatable: bool):
        await ctx.send(f"{class_title}\n{link}\n{name}\n{group}\n{duration}\n{start_time} and the class repeatability is {Repeatable}")
    
"""
    # @cog_ext.cog_subcommand
    #### TODO:
    #### Experiment with subcommands/groups/slash commands, make /calculate in test.py first

def setup(client: commands.Bot):
    client.add_cog(Classes(client))