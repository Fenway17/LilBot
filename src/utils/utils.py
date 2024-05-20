import os
from dotenv import load_dotenv

MASTER_USER_ID = os.getenv("MASTER_USER_ID")  # user id for bot admin


def check_master_user(user_id):
    return int(MASTER_USER_ID) == user_id