import discord
import utils.responses as responses
import cogs.vote.views.utils as utils

CLOSE_TEXT = "Close Vote"
OPEN_TEXT = "Open Vote"


# button to disable all view's buttons to close the vote
class CloseVoteButton(discord.ui.Button):
    def __init__(self):
        self.is_closed = False
        super().__init__(label=CLOSE_TEXT, style=discord.ButtonStyle.red)

    # assumes view has buttons to disable
    # assumes original vote has an embed with an author which is the user id of the vote author

    async def callback(self, interaction: discord.Interaction):
        # check if author is clicking button
        embed = interaction.message.embeds[0]
        if interaction.user.id != int(embed.author.name):
            # prevent non-author from closing vote
            return await interaction.response.send_message(
                responses.USER_NOT_AUTHOR, delete_after=5
            )

        view: discord.ui.View = self.view
        for child in view.children:
            if not self.is_closed and isinstance(child, discord.ui.Button):
                # not closed yet, close buttons
                child.disabled = True
            elif self.is_closed and isinstance(child, discord.ui.Button):
                # closed vote, open buttons
                child.disabled = False

        # toggle is_closed bool to track state
        self.is_closed = not self.is_closed

        if self.is_closed:
            # change button to open vote button
            self.label = OPEN_TEXT
            self.style = discord.ButtonStyle.green
        else:
            # change button to close vote button
            self.label = CLOSE_TEXT
            self.style = discord.ButtonStyle.red
        self.disabled = False  # reenable; disables itself in previous for loop

        await interaction.response.edit_message(embed=embed, view=self.view)
