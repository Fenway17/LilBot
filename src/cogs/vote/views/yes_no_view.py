import discord
from cogs.vote.views.close_vote_button import CloseVoteButton
import cogs.vote.views.utils as utils


class YesNoView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(CloseVoteButton())

    # assumes that the vote contains an embed that has fields that are separated by newlines
    # eg.
    # Andy\n
    # Bob
    # and contains a title/name that has a number to increment
    # eg. YES (0)

    # DO NOT directly alter the embed values as it might lead to errors;
    # use embed.set_field_at()

    @discord.ui.button(
        label="Yes", style=discord.ButtonStyle.green, emoji="👍🏼"
    )  # or .success
    async def green_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # button.disabled=True
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            if "NO" in field.name:
                # remove from "no" vote
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

            if "YES" in field.name:
                # toggle "yes" vote
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

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(
        label="No", style=discord.ButtonStyle.red, emoji="👎🏼"
    )  # or .danger
    async def red_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = interaction.message.embeds[0]
        for field in embed.fields:
            if "YES" in field.name:
                # remove from "yes" vote
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

            if "NO" in field.name:
                # toggle "no" vote
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

        await interaction.response.edit_message(embed=embed, view=self)
