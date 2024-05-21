import discord
from discord.ext import commands
from utils.utils import check_master_user, send_message_not_admin


class Repeat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="repeat", description="Repeats what you say word for word"
    )
    async def repeat(self, ctx, *, arg):  # takes arguments as one big line of text
        await ctx.send(arg)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Repeat(bot))
