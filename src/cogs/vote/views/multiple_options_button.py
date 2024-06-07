import discord
import cogs.vote.views.utils as utils

# button representing an option in a multiple options vote
# displays the number of the option in the vote
class OptionButton(discord.ui.Button):
    def __init__(self, option_number: int, option_label: str, single_only: bool = True):
        self.option_number = option_number
        self.option_label = option_label
        self.single_only = single_only
        super().__init__(label=option_number, style=discord.ButtonStyle.primary)

    # assumes that the vote contains an embed that has fields that are separated by newlines
    # eg.
    # Andy\n
    # Bob

    async def callback(self, interaction: discord.Interaction):
        # self.disabled=True
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            # field name eg. "1) option1 (5)"
            option_title = field.name.split(" ")[1]
            if self.single_only and self.option_label != option_title:
                # remove vote from other fields if single vote only
                if interaction.user.name in field.value:
                    new_name = utils.add_number_to_string(field.name, -1)
                    new_value = utils.remove_user_from_string_list(
                        field.value, interaction.user
                    )
                    embed.set_field_at(
                        embed.fields.index(field),
                        name=new_name,
                        value=new_value,
                        inline=True,
                    )

            if self.option_label == option_title:
                # toggle vote in the field
                if interaction.user.name in field.value:
                    new_name = utils.add_number_to_string(field.name, -1)
                    new_value = utils.remove_user_from_string_list(
                        field.value, interaction.user
                    )
                else:
                    new_name = utils.add_number_to_string(field.name, 1)
                    new_value = utils.add_user_to_string_list(
                        field.value, interaction.user
                    )

                embed.set_field_at(
                    embed.fields.index(field),
                    name=new_name,
                    value=new_value,
                    inline=True,
                )

        await interaction.response.edit_message(embed=embed, view=self.view)