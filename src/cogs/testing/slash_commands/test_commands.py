import os
import discord
from discord import app_commands
from discord.ext import commands
import utils.responses as responses
from utils.permissions import check_developer_user

TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")


# sample slash commands
class TestCommandsSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # Add the guild ids in which the slash command will appear.
    # If it should be in all, remove the argument, but note that
    # it will take some time (up to an hour) to register the
    # command if it's for all guilds.
    @app_commands.command(
        name="hello",
        description="Say Hello!",
    )
    async def test_command(self, interaction: discord.Interaction):
        if not check_developer_user(interaction.user.id):
            await interaction.response.send(
                responses.USER_NO_COMMAND_PERMISSIONS.format(role="developer")
            )
            return

        await interaction.response.send_message("Hello!")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(TestCommandsSlash(bot), guild=discord.Object(id=TEST_SERVER_ID))
