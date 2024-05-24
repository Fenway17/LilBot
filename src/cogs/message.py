import discord
from discord.ext import commands


# TODO: FIX THIS COG
class Message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # used to handle errors
    async def handle_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(f"Invalid input used. Please use correct inputs.", delete_after=5)
        # log the error for debugging
        print(f"Message related error: {error}")

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(name="message", description="User related commands")
    async def message(self, ctx: commands.Context):  
        await ctx.send(f"Please specify subcommands.", delete_after=5)

    @message.command(name="say", description="Says what you say word for word")
    async def say(self, ctx: commands.Context, *, arg):  # takes arguments as one big line of text
        try:
            await ctx.send(arg)
        except Exception as e:
            await self.handle_error(ctx, e)

    # TODO: FIX
    @message.command(name="delete", description="Deletes the latest 0-10 messages")
    async def delete_messages(self, ctx: commands.Context, number: int = 0):
        try:
            if isinstance(ctx.author, discord.Member) and not ctx.author.guild_permissions.manage_messages:
                await ctx.send("You do not have permission to delete messages.")
                return
            
            if number == 0:
                await ctx.send(f"Delete {number} messages...? Huh?", delete_after=5)
                return
            
            message = f"Deleted {number} messages."
            if ctx.interaction: # invoked via slash command
                # defer command; else need to respond in 3 seconds
                await ctx.interaction.response.defer() 
                await ctx.channel.purge(limit=number)
                await ctx.interaction.followup.send(message)
            else: # invoked via regular prefix command
                await ctx.channel.purge(limit=number)
                await ctx.send(message)
        
        except Exception as e:
            await self.handle_error(ctx, e)

        # TODO: UNTESTED
        # TODO: ADD TRY EXCEPT
        @message.command(name="delete_specific", description="Clear X messages from specific user")
        async def delete_specific(self, ctx, interaction: discord.Interaction, member: discord.Member, number: int = 0):
            channel = interaction.channel

            def check_author(m):
                return m.author.id == member.id
            await ctx.channel.purge(limit=number, check=check_author)
            await ctx.send(f"Successfully deleted {number} messages from {member.name}")  

async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Message(bot))
