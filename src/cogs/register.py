import discord
from discord.ext import commands
from discord import app_commands
from database.sqlite_database import SQLiteDatabase
from utils.utils import check_admin_user, send_message_not_admin

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(
    client
)  # TODO: might not be needed due to commands.Bot description


# TODO: TEST IF IT WORKS
class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: SQLiteDatabase = SQLiteDatabase()

    # used to register a given user
    async def database_register(
        self, interaction: discord.Interaction, user: discord.User
    ):
        user_id = str(user.id)
        username = str(user.name)
        if self.db.is_user_registered(user_id):
            await interaction.response.send_message(
                f"{username} is already registered!"
            )
        else:
            self.db.register_user(user_id, username)
            await interaction.response.send_message(f"{username} has been registered!")

    # used to deregister a given user
    async def database_deregister(
        self, interaction: discord.Interaction, user: discord.User
    ):
        user_id = str(user.id)
        username = str(user.name)
        if self.db.is_user_registered(user_id):
            self.db.deregister_user(user_id)
            await interaction.response.send_message(f"{username} is deregistered!")
        else:
            await interaction.response.send_message(
                f"{username} is not even been registered!"
            )

    # used to handle errors
    async def handle_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(
            f"Invalid input used. Please use correct inputs."
        )
        # log the error for debugging
        print(f"Registration error: {error}")

    @app_commands.command(
        name="register_me", description="Registers yourself with LilBot"
    )
    async def register_me(self, interaction: discord.Interaction):
        try:
            await self.database_register(interaction, interaction.user)
        except Exception as e:
            await self.handle_error(interaction, e)

    @app_commands.command(
        name="register_user", description="Registers a given user with LilBot"
    )
    async def register_user(self, interaction: discord.Interaction, user: discord.User):
        try:
            invoker_user_id = interaction.user.id
            if not (check_admin_user(invoker_user_id)):
                send_message_not_admin(interaction)
                return

            await self.database_register(interaction, user)

        except Exception as e:
            await self.handle_error(interaction, e)

    @app_commands.command(
        name="deregister_user", description="Deregisters a given user with LilBot"
    )
    async def deregister_user(
        self, interaction: discord.Interaction, user: discord.User
    ):
        try:
            invoker_user_id = interaction.user.id
            if not (check_admin_user(invoker_user_id)):
                send_message_not_admin(interaction)
                return

            await self.database_deregister(interaction, user)
        except Exception as e:
            await self.handle_error(interaction, e)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Register(bot))
