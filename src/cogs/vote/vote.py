import discord
from discord import app_commands
from discord.ext import commands
from cogs.vote.views.yes_no_view import YesNoView
import utils.responses as responses


class Vote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(name="vote", description="User related commands")
    async def user_group(self, ctx: commands.Context):
        await ctx.send(responses.USER_NO_SUBCOMMANDS, delete_after=5)

    # TODO: ADD a way to close the vote (maybe via timeout)
    @user_group.command(name="yes-no", description="Creates a custom yes/no vote")
    @app_commands.describe(question="Provide a yes/no question")
    async def yes_no(self, ctx: commands.Context, *, question: str):
        view = YesNoView()
        embed = discord.Embed(title=question, description="_Vote OPEN!_")
        embed.add_field(name="---YES (0)---", value="", inline=True)
        embed.add_field(name="---NO (0)---", value="", inline=True)
        await ctx.send(embed=embed, view=view)

    @user_group.command(name="multiple-options", description="Creates a custom vote with multiple options")
    @app_commands.describe(title="Provide a title for the vote")
    @app_commands.describe(options="Provide up to 10 __(comma-separated)__ options to vote on")
    @app_commands.describe(single_only="Force voting for one option only __(default: True)__")
    async def yes_no(self, ctx: commands.Context, title: str, options: str, single_only: bool = True):
        # TODO: IMPLEMENT
        return ctx.send("UNDER CONSTRUCTION")

        option_list = [option.strip() for option in options.split(",")]
        if len(option_list) > 10:
            # prevent creating more than 10 options
            return ctx.send(responses.VOTING_TOO_MANY_OPTIONS.format(number=10), delete_after=10)

        # TODO: CHECK for duplicate options
        pass

async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Vote(bot))
