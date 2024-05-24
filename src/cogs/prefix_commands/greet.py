from discord.ext import commands


# sample regular prefix command group
class Greet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.group(name="greet", pass_context=True)
    async def greet(self, ctx, arg=""):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand.")

    @greet.command(name="hello")
    async def hello(self, ctx, arg=""):
        await ctx.send("Hello!")

    @greet.command(name="goodbye")
    async def goodbye(self, ctx, arg=""):
        await ctx.send("Goodbye!")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Greet(bot))
