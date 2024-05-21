import os
from dotenv import load_dotenv

MASTER_USER_ID = os.getenv("MASTER_USER_ID")  # user id for bot admin


def check_master_user(user_id):
    return int(MASTER_USER_ID) == user_id

async def send_message_not_admin(ctx): # intakes a discord context
    await ctx.send(f"Unable to use command, not an admin user")