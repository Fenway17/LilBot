import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Get the base directory where the .env file is located
base_dir = Path(__file__).resolve().parent.parent

# Load environment variables from .env file in the base directory
load_dotenv(dotenv_path=base_dir / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")
PRIORITY_SERVER_ID = os.getenv("PRIORITY_SERVER_ID")


def get_prefix(bot, message):
    """A callable Prefix. Edited to allow per server prefixes."""

    prefixes = ["$", "#", "lil-bot"]  # may spaces in prefixes

    # Check to see if outside of a guild. e.g DM's etc
    if not message.guild:
        # Only allow certain prefixes to be used in DMs
        return "$"

    # If in a guild, allow the user to mention or use any of the prefixes in the list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix=get_prefix, intents=intents)

initial_extensions = [
    "cogs.testing.prefix_commands.test_commands",
    "cogs.testing.prefix_commands.greet",
    "cogs.testing.slash_commands.test_commands",
    "cogs.testing.hybrid_commands.test_commands",
    "cogs.music.youtube",
    "cogs.music.spotify",
    "cogs.vote.vote",
    "cogs.register",
    "cogs.message",
    "cogs.error_handler",
]


# sync the command tree (slash commands)
async def sync_commands():
    await bot.wait_until_ready()
    # Optionally restrict to specific guild for development; guild=discord.Object(id=TEST_SERVER_ID)
    bot.tree.copy_global_to(guild=discord.Object(id=TEST_SERVER_ID))
    bot.tree.copy_global_to(guild=discord.Object(id=PRIORITY_SERVER_ID))
    # Optionally restrict to specific guild for development; guild=discord.Object(id=TEST_SERVER_ID)
    await bot.tree.sync(guild=discord.Object(id=TEST_SERVER_ID))
    await bot.tree.sync(guild=discord.Object(id=PRIORITY_SERVER_ID))
    # bot.tree.clear_commands(guild=None) # clear entire slash command tree; used for removing all slash commands
    # await bot.tree.sync() # global sync; takes significantly longer to update


# load all cogs / extensions
async def load_cog_extensions():
    for extension in initial_extensions:  # add cogs (command files)
        try:
            await bot.load_extension(extension)
            print(f"Loaded to cog: '{extension}'")
        except Exception as e:
            print(f"Failed to load cog '{extension}': {e}")
    print(f"Loaded all extensions.")


@bot.event
async def on_ready():  # called when the bot is logged in and ready
    # load extensions / sync slash commands
    await load_cog_extensions()
    await bot.loop.create_task(sync_commands())

    # Changes bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(
        activity=discord.Game(
            name="In development", type=1, url="https://github.com/Fenway17/LilBot"
        )
    )

    print(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nDiscord version: {discord.__version__}\n"
    )


# TODO: remove this; breaks commands due to 'intercepting' the messages that contains the commands
# @bot.event
# async def on_message(message):  # called when the bot receives a message
#     if message.author == bot.user:  # check if author is the bot itself
#         return

#     if message.content.startswith("$hello"):
#         await message.channel.send("Hello!")


bot.run(BOT_TOKEN)  # runs the bot
