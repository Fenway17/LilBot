import re
import discord

# adds a number to the first string of numbers in a string and returns new string
def add_number_to_string(full_string: str, number: int):
    # find the number in the string
    match = re.search(r"(\d+)", full_string)  # match to a string of digits
    if match:
        # Extract the number
        initial_number = int(match.group(1))
        incremented_number = initial_number + number
        # replace the old number
        return full_string.replace(str(initial_number), str(incremented_number))

    return full_string

# adds a discord user to a list string separated by "\n" newlines and returns new string
def add_user_to_string_list(list_string: str, user: discord.User):
    return list_string + "\n" + user.display_name + " (" + user.name + ")"

# removes a discord user to a list string separated by "\n" newlines and returns new string
def remove_user_from_string_list(list_string: str, user: discord.User):
    string_list = list_string.split("\n")
    # exclude matching user from the list (matched by username)
    filtered_list = [
        user_string for user_string in string_list if user.name not in user_string
    ]
    return "\n".join(filtered_list)