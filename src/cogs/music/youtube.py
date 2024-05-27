import re
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

YOUTUBE_URL_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
)

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # Bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


# TODO: TEST if it works
# TODO: ADD delete_after AND/OR ephemeral AND/OR silent to some messages to prevent clogging of channel
class YoutubeMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

        # dictionary with keys: guild ids and values: list of (song url, title)
        self.song_queue = {}
        # dictionary with keys: guild ids and value: (song url, title)
        # used in edge case where playlist is cleared while song is still playing
        self.current_song = {}
        # dictionary with keys: guild ids and value: queue index
        self.current_song_index = {}
        # dictionary with keys: guild ids and value: bool
        self.repeat_mode = {}

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(
        name="youtube", description="Youtube player related commands"
    )
    async def youtube(self, ctx: commands.Context):
        await ctx.send(f"Please specify subcommands.", delete_after=5)

    @youtube.command(name="join", help="Join the voice channel")
    async def join(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send("You're not connected to a voice channel!")
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.send("Moving to your voice channel!")
            return await ctx.voice_client.move_to(channel)

        await channel.connect(self_deaf=True)
        await ctx.send("Joined your voice channel!")

    @youtube.command(name="leave", help="Leave the voice channel")
    async def leave(self, ctx: commands.Context):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            return await ctx.send("Leaving your voice channel!")

        await ctx.send("I'm not connected to a voice channel!")

    # main command logic of adding youtube videos to queue
    @youtube.command(name="play", help="Play a song from YouTube")
    async def play(self, ctx: commands.Context, *, search: str = None):
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        if ctx.guild.id not in self.song_queue:
            # initialize new song queue for guild
            self.song_queue[ctx.guild.id] = []
            # initialize to -1; play next function increments this
            self.current_song_index[ctx.guild.id] = -1
            self.repeat_mode[ctx.guild.id] = False

        if search:
            # Check if search input is a URL
            if not YOUTUBE_URL_REGEX.match(search):
                # If not a URL, search for the video
                search = f"ytsearch:{search}"

            # parse into YDL and input into song queue
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search, download=False)
                if "entries" in info:
                    # given after a search (instead of direct url)
                    info = info["entries"][0]  # Take the first result from the search
                url2 = info["formats"][0]["url"]
                title = info.get("title", "Unknown Title")
                # set to silent to prevent spam notifications
                await ctx.send(f"Added to queue: {title}", silent=True)
                # add to playlist
                self.song_queue[ctx.guild.id].append((url2, title))

        if not ctx.voice_client.is_playing():
            # start playing next song in queue
            await self.play_next(ctx)
        else:
            await ctx.send(
                f"Currently playing: {self.current_song[ctx.guild.id][1]}", silent=True
            )

    # main logic of playing youtube videos in queue
    async def play_next(self, ctx: commands.Context):
        # check if song queue exists and is not empty
        if ctx.guild.id in self.song_queue and len(self.song_queue[ctx.guild.id]) > 0:
            # check repeat mode and increment current song index accordingly
            if self.repeat_mode[ctx.guild.id]:
                # incremented index will loop back to 0 if at end of queue
                self.current_song_index[ctx.guild.id] = (
                    self.current_song_index[ctx.guild.id] + 1
                ) % len(self.song_queue[ctx.guild.id])
            else:
                # increment normally
                self.current_song_index[ctx.guild.id] += 1

            # check if next index is under queue length
            if self.current_song_index[ctx.guild.id] < len(
                self.song_queue[ctx.guild.id]
            ):
                # extract url and title from song queue
                next_song_url, next_song_title = self.song_queue[ctx.guild.id][
                    self.current_song_index[ctx.guild.id]
                ]
                # update current song
                self.current_song[ctx.guild.id] = (next_song_url, next_song_title)
                # stop and then play voice client
                ctx.voice_client.stop()
                ctx.voice_client.play(
                    discord.FFmpegPCMAudio(next_song_url, **FFMPEG_OPTIONS),
                    after=lambda e: self.bot.loop.create_task(self.play_next(ctx)),
                )
                await ctx.send(f"Now playing: {next_song_title}", silent=True)
            else:
                # do not continue playing music
                # remove current song record since no music is playing
                self.current_song.pop(ctx.guild.id, None)
                # end of queue, reset to -1 to be incremented by play next function
                self.current_song_index[ctx.guild.id] = -1
        else:
            # queue is empty or does not exist; remove current song record
            self.current_song.pop(ctx.guild.id, None)
            await ctx.send("The queue is empty, add more songs!")

    @youtube.command(name="pause", help="Pause the song")
    async def pause(self, ctx: commands.Context):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the song")
        else:
            await ctx.send("No song is playing")

    @youtube.command(name="resume", help="Resume the song")
    async def resume(self, ctx: commands.Context):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed the song")
        else:
            await ctx.send("The song is not paused")

    @youtube.command(name="stop", help="Stop the song")
    async def stop(self, ctx: commands.Context):
        ctx.voice_client.stop()
        self.current_song.pop(ctx.guild.id, None)  # Remove current song on stop
        await ctx.send("Stopped the player")

    @youtube.command(name="next", help="Play the next song in the queue")
    async def next(self, ctx: commands.Context):
        await self.play_next(ctx)

    @youtube.command(name="goto", help="Play the song at the queue index")
    async def goto(self, ctx: commands.Context, index: int):
        if ctx.guild.id in self.song_queue and 0 <= index - 1 < len(
            self.song_queue[ctx.guild.id]
        ):
            # move the index tracker to song before the target song
            self.current_song_index[ctx.guild.id] = index - 2
            await self.play_next(ctx)
        else:
            await ctx.send("Invalid queue number!")

    @youtube.command(name="repeat", help="Toggle repeat mode")
    async def repeat(self, ctx):
        if ctx.guild.id not in self.song_queue:
            self.song_queue[ctx.guild.id] = []
            self.repeat_mode[ctx.guild.id] = False

        self.repeat_mode[ctx.guild.id] = not self.repeat_mode[ctx.guild.id]
        await ctx.send(
            f"Repeat mode is now {'on' if self.repeat_mode[ctx.guild.id] else 'off'}!"
        )

    @youtube.command(name="clear", help="Clear the playlist")
    async def clear(self, ctx):
        if ctx.guild.id in self.song_queue:
            self.song_queue[ctx.guild.id] = []
            self.current_song_index[ctx.guild.id] = 0
            # note: current song record is not cleared
            await ctx.send("Cleared the playlist!")
        else:
            await ctx.send("No playlist to clear!")

    @youtube.command(name="playlist", help="Show the current playlist")
    async def playlist(self, ctx):
        if ctx.guild.id in self.song_queue and len(self.song_queue[ctx.guild.id]) > 0:
            playlist = "\n".join(
                [
                    f"{index + 1}. {title}"
                    for index, (url, title) in enumerate(self.song_queue[ctx.guild.id])
                ]
            )
            await ctx.send(f"Current playlist:\n{playlist}")
        else:
            await ctx.send("The playlist is empty!")

    @youtube.hybrid_command(
        name="current", description="Displays the current song and playlist index"
    )
    async def current(self, ctx: commands.Context):
        if ctx.guild.id in self.current_song:
            current_song_url, current_song_title = self.current_song[ctx.guild.id]
            await ctx.send(f"Currently playing: {current_song_title}")
        else:
            await ctx.send("No song is currently playing!")

    @youtube.command(name="remove", help="Remove a song from the playlist by index")
    async def remove(self, ctx, index: int):
        if ctx.guild.id in self.song_queue and 0 <= index - 1 < len(
            self.song_queue[ctx.guild.id]
        ):
            removed_song = self.song_queue[ctx.guild.id].pop(index - 1)
            await ctx.send(f"Removed from playlist: {removed_song[1]}")
            if self.current_song_index[ctx.guild.id] >= index - 1:
                self.current_song_index[ctx.guild.id] -= 1
        else:
            await ctx.send("Invalid queue number!")


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(YoutubeMusic(bot))
