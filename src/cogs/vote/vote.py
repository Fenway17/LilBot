import discord
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

    @user_group.command(name="yes-no", description="Creates a custom yes/no vote")
    async def yes_no(self, ctx: commands.Context, *, question: str):
        view=YesNoView()
        embed = discord.Embed(title=question, description="_Vote below!_")
        embed.add_field(name="---Yes---", value="__Total: 0__", inline=True)
        embed.add_field(name="---No---", value="__Total: 0__", inline=True)
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Vote(bot))