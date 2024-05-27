import discord
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    def is_from_bot(self, message: discord.Message) -> bool:
        print(f"author = {message.author.id} \nbotid = {self.bot.user.id}")
        return message.author.id == self.bot.user.id

    def is_not_from_bot(self, message: discord.Message) -> bool:
        return not self.is_from_bot(message)

    # used to handle errors
    async def handle_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(
            f"Invalid input used. Please use correct inputs.", delete_after=5
        )
        # log the error for debugging
        print(f"Message related error: {error}")

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(name="message", description="User related commands")
    async def message(self, ctx: commands.Context):
        await ctx.send(f"Please specify subcommands.", delete_after=5)

    @message.command(name="say", description="Says what you say word for word")
    async def say(
        self, ctx: commands.Context, *, arg
    ):  # takes arguments as one big line of text
        try:
            await ctx.send(arg)
        except Exception as e:
            await self.handle_error(ctx, e)

    @message.command(name="delete", description="Deletes the latest 0-10 messages")
    async def delete_messages(
        self, ctx: commands.Context, number: int, member: discord.Member = None
    ):
        try:
            if (
                isinstance(ctx.author, discord.Member)
                and not ctx.author.guild_permissions.manage_messages
            ):
                await ctx.send("You do not have permission to delete messages.")
                return

            if number <= 0:
                await ctx.send(f"Delete {number} messages...? Huh?", delete_after=5)
                return

            if number > 10:
                number = 10

            if ctx.interaction:  # invoked via slash command
                # defer command; else need to respond in 3 seconds
                await ctx.interaction.response.defer()
                deleted_messages = await ctx.channel.purge(
                    limit=number, before=ctx.interaction.created_at
                )
                # await ctx.interaction.followup.send(f"Deleted {len(deleted_messages)} messages.")
                await ctx.send(
                    f"Deleted {len(deleted_messages)} messages.", delete_after=5
                )
            else:  # invoked via regular prefix command
                deleted_messages = await ctx.channel.purge(limit=number)
                await ctx.send(
                    f"Deleted {len(deleted_messages)} messages.", delete_after=5
                )

        except Exception as e:
            await self.handle_error(ctx, e)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Message(bot))
