from discord.ext import commands


# TODO: UNUSED; discord.py handles it for the bot using ctx.send()
# hybrid messages use Context that may contain an Interaction
async def send_message_hybrid(ctx: commands.Context, message: str):
    if ctx.interaction:  # slash commands
        await ctx.interaction.response.send_message(message)
    else:
        await ctx.send(message)
