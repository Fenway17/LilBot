import os
import discord
from discord.ext import commands
import utils.responses as responses
from utils.permissions import check_developer_user

TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")


# sample hybrid commands
class TestCommandsHybrid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # hybrid commands contain a commands.Context which may contain a discord.Interaction
    # if invoked via slash commands instead of regular prefix command, which otherwise
    # contains None
    @commands.hybrid_command(
        name="hybrid-test", description="Test single argument input"
    )
    async def test_single(self, ctx: commands.Context, arg):
        if not check_developer_user(ctx.author.id):
            await ctx.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="developer")
            )
            return
        await ctx.send(f"argument: {arg}")

    @commands.hybrid_command(
        name="hybrid-test2", description="Test multiple argument input as a keyword"
    )
    async def test_keyword(
        self, ctx, *, arg
    ):  # takes arguments as one big line of text
        if not check_developer_user(ctx.author.id):
            await ctx.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="developer")
            )
            return

        await ctx.send(arg)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(TestCommandsHybrid(bot), guild=discord.Object(id=TEST_SERVER_ID))
