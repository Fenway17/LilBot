import os
from typing import Union
import discord
from discord.ext import commands
from dotenv import load_dotenv

MASTER_USER_ID = os.getenv("MASTER_USER_ID")  # user id for bot admin


def check_master_user(user_id):
    return int(MASTER_USER_ID) == user_id


def check_admin_user(user_id):
    if check_master_user(user_id):
        return True
    # TODO: add checks for admin users as well
    return False


# TODO: TEST IF IT WORKS
async def send_message_not_admin(
    ctx_or_interaction: Union[commands.Context, discord.Interaction]
):
    # intakes either discord commands context or discord interactions
    if isinstance(
        ctx_or_interaction, commands.Context
    ):  # related to regular prefix commands
        ctx = ctx_or_interaction
        await ctx.send(f"Unable to use command, not an admin user")
    elif isinstance(
        ctx_or_interaction, discord.Interaction
    ):  # related to slash command interactions
        interaction = ctx_or_interaction
        await interaction.response.send_message(f"This is a slash command!")
    else:
        raise ValueError("Invalid argument type")
