import os
import discord
from discord.ext import commands
import utils.responses as responses
from utils.permissions import check_developer_user

TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")


# sample regular prefix commands
class TestCommandsPrefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(name="test", description="Test multiple arguments input")
    async def test_multiple(self, ctx, *args):
        if not check_developer_user(ctx.author.id):
            await ctx.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="developer")
            )
            return

        arguments = ", ".join(args)
        await ctx.send(f"{len(args)} arguments: {arguments}")

    @commands.command(
        name="test2", description="Test multiple arguments input as keyword"
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
    await bot.add_cog(TestCommandsPrefix(bot), guild=discord.Object(id=TEST_SERVER_ID))
