from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error
    ):  # handles errors for regular prefix commands
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing input. Please provide inputs.", delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "Bad input. Please provide correct types of inputs.", delete_after=10
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Error invoking the command.", delete_after=10)
        else:
            await ctx.send(
                "Error occurred while processing the command.", delete_after=10
            )
        # log the error for debugging
        print(f"Prefix command error: {error}")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(ErrorHandler(bot))
