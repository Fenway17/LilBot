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
    ctx: commands.Context,
    role: str = "admin",
):
    message = f"Unable to use command, not {role} user."
    await ctx.send(message)
