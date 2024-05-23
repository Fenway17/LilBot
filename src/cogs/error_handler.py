from discord.ext import commands


# TODO: TEST IF IT WORKS
class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx, error
    ):  # handles errors for regular prefix commands
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing required argument. Please check your input and try again."
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "Bad argument. Please provide the correct type of arguments."
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error invoking the command.")
        else:
            await ctx.send("An error occurred while processing the command.")
        # log the error for debugging
        print(f"Prefix command error: {error}")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(ErrorHandler(bot))
