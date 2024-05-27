import os
from typing import Union
import discord
from discord.ext import commands
from database.sqlite_database import SQLiteDatabase


MASTER_USER_ID = os.getenv("MASTER_USER_ID")  # user id for bot admin
db: SQLiteDatabase = SQLiteDatabase()


def check_master_user(user_id: int):  # checks for bot creator or other master users
    if int(MASTER_USER_ID) == user_id or db.get_user_role(user_id) == "master":
        return True
    return False


def check_developer_user(user_id: int):
    if check_master_user(user_id) or db.get_user_role(user_id) == "developer":
        return True
    return False


def check_admin_user(user_id):  # checks for server/guild admins
    if check_developer_user(user_id):
        return True
    # TODO: add checks for admin users as well
    return False


async def send_message_not_role(
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
    role: str = "admin",
):
    message = f"Unable to use command, not {role} user."
    # intakes either discord commands context or discord interactions
    if isinstance(ctx_or_interaction, commands.Context):
        # related to regular prefix commands
        ctx = ctx_or_interaction
        if ctx.interaction:
            # related to hybrid commands (they use both context and interactions)
            await interaction.response.send_message(message)
        else:  # is actually a regular prefix command
            await ctx.send(message)
    elif isinstance(ctx_or_interaction, discord.Interaction):
        # related to slash command interactions
        interaction = ctx_or_interaction
        await interaction.response.send_message(message)
    else:
        raise ValueError("Invalid argument type.")
