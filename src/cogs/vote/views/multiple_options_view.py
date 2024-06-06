from typing import List
import discord
from cogs.vote.views.multiple_options_button import OptionButton
import cogs.vote.views.utils as utils

class MultipleOptionsView(discord.ui.View):
    def __init__(self, options: List[str], timeout=None, single_only: bool = True):
        self.options = options
        super().__init__(timeout=timeout)
        for index, option in enumerate(options):
            self.add_item(OptionButton(option_number=index+1, option_label=option, single_only=single_only))

    

    
