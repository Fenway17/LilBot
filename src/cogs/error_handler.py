from discord.ext import commands
import utils.responses as responses


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error
    ):  # handles errors for regular prefix commands
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(responses.USER_MISSING_INPUT, delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(responses.USER_INVALID_INPUT, delete_after=10)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(responses.BOT_INVOKE_COMMAND_ERROR, delete_after=10)
        else:
            await ctx.send(responses.BOT_PROCESS_COMMAND_ERROR, delete_after=10)
        # log the error for debugging
        print(f"Command error: {error}")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(ErrorHandler(bot))
