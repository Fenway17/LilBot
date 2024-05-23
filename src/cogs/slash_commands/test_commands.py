import os
import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import check_master_user, send_message_not_admin

TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(
    client
)  # TODO: might not be needed due to commands.Bot description


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
        await interaction.response.send_message("Hello!")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(TestCommandsSlash(bot), guild=discord.Object(id=TEST_SERVER_ID))
