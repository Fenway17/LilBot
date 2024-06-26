from typing import List
import discord
from cogs.vote.views.close_vote_button import CloseVoteButton
from cogs.vote.views.multiple_options_button import OptionButton


# view containing all the buttons for a multiple options vote
class MultipleOptionsView(discord.ui.View):
    def __init__(
        self, options: List[str], author_id, timeout=None, single_only: bool = True
    ):
        super().__init__(timeout=timeout)
        self.options = options
        self.author_id = author_id
        for index, option in enumerate(options):
            self.add_item(
                OptionButton(
                    option_number=index + 1,
                    option_label=option,
                    single_only=single_only,
                )
            )
        self.add_item(CloseVoteButton(author_id))
