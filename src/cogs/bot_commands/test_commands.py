import discord
from discord.ext import commands
from utils.utils import check_master_user


class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    intents = discord.Intents.default()
    intents.message_content = True

    @commands.command(name="test")
    async def test_multiple(self, ctx, *args):
        if not check_master_user(ctx.author.id):
            await send_message_not_admin(ctx)
            return

        arguments = ", ".join(args)
        await ctx.send(f"{len(args)} arguments: {arguments}")

    @commands.command(name="test2")
    async def test_keyword(
        self, ctx, *, arg
    ):  # takes arguments as one big line of text
        if not check_master_user(ctx.author.id):
            await send_message_not_admin(ctx)
            return

        await ctx.send(arg)


async def setup(bot):  # required for adding cog to the bot
    await bot.add_cog(TestCommands(bot))


async def send_message_not_admin(ctx):
    await ctx.send(f"Unable to use command, not an admin user")
