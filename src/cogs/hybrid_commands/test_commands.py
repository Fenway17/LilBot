import os
import discord
from discord.ext import commands
from utils.utils import check_master_user, send_message_not_admin

TEST_SERVER_ID = os.getenv('TEST_SERVER_ID')

class TestCommandsHybrid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="hybrid-test")
    async def test_single(self, ctx, arg):
        if not check_master_user(ctx.author.id):
            await send_message_not_admin(ctx)
            return
        
        await ctx.send(f"argument: {arg}")

    @commands.hybrid_command(name="hybrid-test2")
    async def test_keyword(
        self, ctx, *, arg
    ):  # takes arguments as one big line of text
        if not check_master_user(ctx.author.id):
            await send_message_not_admin(ctx)
            return

        await ctx.send(arg)

async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(TestCommandsHybrid(bot))