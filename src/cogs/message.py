import discord
from discord.ext import commands
from discord import app_commands
import utils.responses as responses
from utils.permissions import check_admin_user


class Message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    def is_from_bot(self, message: discord.Message) -> bool:
        print(f"author = {message.author.id} \nbotid = {self.bot.user.id}")
        return message.author.id == self.bot.user.id

    def is_not_from_bot(self, message: discord.Message) -> bool:
        return not self.is_from_bot(message)

    # TODO: REMOVE, errors handled by different class
    # # used to handle errors
    # async def handle_error(self, ctx: commands.Context, error: Exception):
    #     await ctx.send(responses.USER_INVALID_INPUT, delete_after=5)
    #     # log the error for debugging
    #     print(f"Message related error: {error}")

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(name="message", description="User related commands")
    async def message(self, ctx: commands.Context):
        await ctx.send(responses.USER_NO_SUBCOMMANDS, delete_after=5)

    @message.command(name="say", description="Says what you say word for word")
    @app_commands.describe(sentence="No slurs pl0x uwu owo")
    async def say(
        self, ctx: commands.Context, *, sentence
    ):  # takes arguments as one big line of text
        await ctx.send(sentence)

    # TODO: add functionality to delete specific user's messages
    @message.command(name="delete", description="Deletes the latest 0-10 messages")
    @app_commands.describe(number="Number between 0-10")
    @app_commands.describe(member="<currently not working>")
    async def delete_messages(
        self, ctx: commands.Context, number: int, member: discord.Member = None
    ):
        if not check_admin_user(ctx.author.id) and (
            isinstance(ctx.author, discord.Member)
            and not ctx.author.guild_permissions.manage_messages
        ):
            await ctx.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="admin")
            )
            return

        if number <= 0:
            await ctx.send(
                responses.MESSAGE_INVALID_DELETE.format(number=number), delete_after=5
            )
            return

        if number > 10:
            number = 10

        # defer command; else need to respond in 3 seconds
        await ctx.defer()  # defers response if slash command was used
        deleted_messages = await ctx.channel.purge(
            limit=number, before=ctx.interaction.created_at
        )
        await ctx.send(responses.MESSAGE_DELETED.format(number=len(deleted_messages)), delete_after=5)

    @message.command(name="clean", description="Deletes bot's messages in the last 100 (default) messages")
    @app_commands.describe(number="Number between 0-100")
    async def clean_messages(self, ctx: commands.Context, number: int = 100):
        if not check_admin_user(ctx.author.id) and (
            isinstance(ctx.author, discord.Member)
            and not ctx.author.guild_permissions.manage_messages
        ):
            await ctx.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="admin")
            )
            return

        if number <= 0:
            await ctx.send(
                responses.MESSAGE_INVALID_DELETE.format(number=number), delete_after=5
            )
            return

        if number > 100:
            number = 100

        # defer command; else need to respond in 3 seconds
        await ctx.defer()  # defers response if slash command was used
        deleted_messages = await ctx.channel.purge(
            limit=number, before=ctx.interaction.created_at, check=self.is_bot_author,
        )
        await ctx.send(responses.MESSAGE_DELETED.format(number=len(deleted_messages)), delete_after=5)

    def is_bot_author(self, message: discord.Message):
        return message.author.id == self.bot.user.id

async def setup(bot: commands.Bot) -> bool:  # required for adding cog to the bot
    await bot.add_cog(Message(bot))
