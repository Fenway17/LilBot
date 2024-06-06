import re
import discord


class YesNoView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    # assumes that the vote contains an embed that has fields that are separated by newlines
    # eg.
    # Total: 2\n
    # Andy\n
    # Bob

    # adds a number to the first string of numbers in a string and returns new string
    def add_number_to_string(self, full_string: str, number: int):
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
    def add_user_to_string_list(self, list_string: str, user: discord.User):
        return list_string + "\n" + user.display_name + " (" + user.name + ")"

    # removes a discord user to a list string separated by "\n" newlines and returns new string
    def remove_user_from_string_list(self, list_string: str, user: discord.User):
        string_list = list_string.split("\n")
        # exclude matching user from the list (matched by username)
        filtered_list = [
            user_string for user_string in string_list if user.name not in user_string
        ]
        return "\n".join(filtered_list)

    @discord.ui.button(
        label="Yes", style=discord.ButtonStyle.green, emoji="👍🏼"
    )  # or .success
    async def green_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # button.disabled=True
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            if field.name == "---No---":
                # remove from "no" vote
                if interaction.user.name in field.value:
                    new_value = self.add_number_to_string(field.value, -1)
                    new_value = self.remove_user_from_string_list(
                        new_value, interaction.user
                    )
                    embed.set_field_at(
                        embed.fields.index(field),
                        name="---No---",
                        value=new_value,
                        inline=True,
                    )

            if field.name == "---Yes---":
                # toggle "yes" vote
                if interaction.user.name in field.value:
                    new_value = self.add_number_to_string(field.value, -1)
                    new_value = self.remove_user_from_string_list(
                        new_value, interaction.user
                    )
                else:
                    new_value = self.add_number_to_string(field.value, 1)
                    new_value = self.add_user_to_string_list(
                        new_value, interaction.user
                    )

                embed.set_field_at(
                    embed.fields.index(field),
                    name="---Yes---",
                    value=new_value,
                    inline=True,
                )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="No", style=discord.ButtonStyle.red, emoji="👎🏼"
    )  # or .danger
    async def red_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            if field.name == "---Yes---":
                # remove from "yes" vote
                if interaction.user.name in field.value:
                    new_value = self.add_number_to_string(field.value, -1)
                    new_value = self.remove_user_from_string_list(
                        new_value, interaction.user
                    )
                    embed.set_field_at(
                        embed.fields.index(field),
                        name="---Yes---",
                        value=new_value,
                        inline=True,
                    )

            if field.name == "---No---":
                # toggle "no" vote
                if interaction.user.name in field.value:
                    new_value = self.add_number_to_string(field.value, -1)
                    new_value = self.remove_user_from_string_list(
                        new_value, interaction.user
                    )
                else:
                    new_value = self.add_number_to_string(field.value, 1)
                    new_value = self.add_user_to_string_list(
                        new_value, interaction.user
                    )

                embed.set_field_at(
                    embed.fields.index(field),
                    name="---No---",
                    value=new_value,
                    inline=True,
                )

        await interaction.response.edit_message(embed=embed, view=self)
