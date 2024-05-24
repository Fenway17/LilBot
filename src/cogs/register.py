import discord
from discord.ext import commands
from database.sqlite_database import SQLiteDatabase, valid_roles
from utils.permissions import check_master_user, send_message_not_role


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.db: SQLiteDatabase = SQLiteDatabase()

    # used to register a given user
    async def database_register(self, ctx: commands.Context, user: discord.User, role: str = "user"):
        user_id = user.id
        username = user.name
        if self.db.is_user_registered(user_id):
            await ctx.send(f"{username} is already registered!")
        else:
            self.db.register_user(user_id, username, role)
            await ctx.send(f"{username} has been registered!")

    # used to deregister a given user
    async def database_deregister(self, ctx: commands.Context, user: discord.User):
        user_id = user.id
        username = user.name
        if self.db.is_user_registered(user_id):
            self.db.deregister_user(user_id)
            await ctx.send(f"{username} is deregistered!")
        else:
            await ctx.send(f"{username} is not even registered!")

    # used to handle errors
    async def handle_error(self, ctx: commands.Context, error: Exception):
        await ctx.send(f"Invalid input used. Please use correct inputs.", delete_after=5)
        # log the error for debugging
        print(f"Registration related error: {error}")

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(name="user", description="User related commands")
    async def user_group(self, ctx: commands.Context):  
        await ctx.send(f"Please specify subcommands.", delete_after=5)

    @user_group.command(name="register_me", description="Registers yourself with LilBot")
    async def register_me(self, ctx: commands.Context):
        try:
            await self.database_register(ctx, ctx.author)
        except Exception as e:
            await self.handle_error(ctx, e)

    @user_group.command(
        name="register_user", description="Registers a given user with LilBot"
    )
    async def register_user(self, ctx: commands.Context, user: discord.User, role: str = "user"):
        try:
            invoker_user_id = ctx.author.id
            if not (check_master_user(invoker_user_id)):
                await send_message_not_role(ctx, "master")
                return

            await self.database_register(ctx, user)

        except Exception as e:
            await self.handle_error(ctx, e)

    @user_group.command(
        name="deregister_user", description="Deregisters a given user with LilBot"
    )
    async def deregister_user(self, ctx: commands.Context, user: discord.User):
        try:
            invoker_user_id = ctx.author.id
            if not (check_master_user(invoker_user_id)):
                await send_message_not_role(ctx, "master")
                return

            await self.database_deregister(ctx, user)
        except Exception as e:
            await self.handle_error(ctx, e)

    @user_group.command(
        name="update_user_role", description="Updates someone's user role"
    )
    async def update_user_role(
        self, ctx: commands.Context, user: discord.User, role: str
    ):
        try:
            invoker_user_id = ctx.author.id
            if not (check_master_user(invoker_user_id)):
                await send_message_not_role(ctx, "master")
                return

            if not self.db.is_user_registered(user.id):
                await ctx.send(f"{user.name} is not even registered!")
                return

            self.db.update_user_role(user.id, role)
            await ctx.send(f"{user}'s role has been updated to {role}.")
        except Exception as e:
            await self.handle_error(ctx, e)

    @user_group.command(name="user_info", description="Gets user's information")
    async def user_info(self, ctx: commands.Context, user: discord.User):
        try:
            if not self.db.is_user_registered(user.id):
                await ctx.send(f"{user.name} is not even registered!")
                return
            
            user_role = self.db.get_user_role(user.id)
            await ctx.send(f"User info for {user.name}:\nRole: {user_role}")
            # TODO: more user info logic here
        except Exception as e:
            await self.handle_error(ctx, e)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(Register(bot))
