import re
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

from utils.permissions import check_developer_user, send_message_not_role

YOUTUBE_URL_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
)

YOUTUBE_PLAYLIST_URL_REGEX = re.compile(
    r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.*(list=.+)$')

# ydl_opts = {
#     "format": "bestaudio/best",
#     "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
#     "restrictfilenames": True,
#     "noplaylist": True,
#     "nocheckcertificate": True,
#     "ignoreerrors": False,
#     "logtostderr": False,
#     "quiet": True,
#     "no_warnings": True,
#     "default_search": "auto",
#     "source_address": "0.0.0.0",  # Bind to ipv4 since ipv6 addresses cause issues sometimes
# }

ydl_opts = {"format": "bestaudio", "noplaylist": "True", "quiet": True}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


# TODO: ADD delete_after AND/OR ephemeral AND/OR silent to some messages to prevent clogging of channel
# TODO: TEST if it works in >= 2 servers at the same time
# uses asyncio loop to repeatedly call play_next each cycle to ensure the bot goes through
# its list of songs it records
class YoutubeMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.volume = 0.20

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
        await ctx.send(f"Please specify subcommands.", silent=True, delete_after=5)

    @youtube.command(name="join", help="Join the voice channel")
    async def join(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send(
                "You're not connected to a voice channel!", silent=True, delete_after=5
            )
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            # already in a channel somewhere
            await ctx.send("Moving to your voice channel!", silent=True)
            return await ctx.voice_client.move_to(channel)

        await channel.connect(
            self_deaf=True
        )  # ctx.voice_client will now have a discord.VoiceClient
        await ctx.send("Joined your voice channel!", silent=True)

    @youtube.command(name="leave", help="Leave the voice channel")
    async def leave(self, ctx: commands.Context):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            return await ctx.send("Leaving voice channel!")

        await ctx.send("I'm not connected to a voice channel!", silent=True)

    # main command logic of adding youtube videos to queue
    @youtube.command(name="play", help="Play a song from YouTube")
    async def play(self, ctx: commands.Context, *, search: str = None):
        print(f"play attempt")
        await ctx.defer()  # defers response if slash command used

        if not ctx.voice_client:
            # attempt to join a channel
            await ctx.invoke(self.join)
            # if successful, ctx.voice_client would have a discord.VoiceClient

        if not ctx.voice_client:
            # still not in a channel; stop this command
            return

        if ctx.guild.id not in self.song_queue:
            print(f"initialize queue")
            # initialize new song queue for guild
            self.song_queue[ctx.guild.id] = []
            # initialize to -1; play next function increments this
            self.current_song_index[ctx.guild.id] = -1
            self.repeat_mode[ctx.guild.id] = False

        

        if search:
            print(f"searching for youtube video")
            # Check if search input is a URL
            is_playlist_url = YOUTUBE_PLAYLIST_URL_REGEX.match(search)
            is_video_url = YOUTUBE_URL_REGEX.match(search)
            if not is_playlist_url and not is_video_url:
                # If not a URL, search for the video
                search = f"ytsearch:{search}"

            # extract_flat to extract minimal info
            ydl_opts_used = {
                **ydl_opts,
                'extract_flat': 'in_playlist' if is_playlist_url else False,
            }

            # parse into YDL and input into song queue
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search, download=False)
                if "entries" in info:
                    # info is multiple entries
                    # entries given after a keyword search or playlist url search
                    entries = info["entries"] # take all entries
                else:
                    # info is a single entry
                    entries = [info] # make into single item list

                # add all entries to playlist
                for entry in entries:
                    url2 = entry["url"]
                    title = entry.get("title", "Unknown Title")
                    print(f"url2 = {url2}; title = {title}")
                    # add to playlist
                    self.song_queue[ctx.guild.id].append((url2, title))

                # inform user
                if is_playlist_url:
                    playlist_title = info.get('title', 'Unknown Playlist')
                    await ctx.send(f"Added playlist to queue: {playlist_title}")
                else:
                    video_title = entries[0].get('title', 'Unknown Title')
                    await ctx.send(f"Added to queue: {video_title}")

        # attempt to play music
        if not ctx.voice_client.is_playing():
            print(f"playing next song")
            # start playing next song in queue
            await self.play_next(ctx)
        elif not search:
            # already playing song, and command was not a search
            print(f"already playing song")
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
            if (
                0
                <= self.current_song_index[ctx.guild.id]
                < len(self.song_queue[ctx.guild.id])
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
                    discord.PCMVolumeTransformer(
                        discord.FFmpegPCMAudio(next_song_url, **FFMPEG_OPTIONS),
                        volume=self.volume,
                    ),
                    after=lambda e: self.bot.loop.create_task(self.play_next(ctx)),
                )
                await ctx.send(f"Now playing: {next_song_title}")
            else:
                # do not continue playing music
                # remove current song record since no music is playing
                self.current_song.pop(ctx.guild.id, None)
                # end of queue, set to last element of playlist to be incremented by play next function
                self.current_song_index[ctx.guild.id] = (
                    len(self.song_queue[ctx.guild.id]) - 1
                )
                await ctx.send(f"End of playlist!", silent=True)
        else:
            # queue is empty or does not exist; remove current song record
            self.current_song.pop(ctx.guild.id, None)
            await ctx.send("The queue is empty, add more songs!", silent=True)

    @youtube.command(name="pause", help="Pause the music player")
    async def pause(self, ctx: commands.Context):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the music player!")
        else:
            await ctx.send("No music is playing!", silent=True)

    @youtube.command(name="resume", help="Resume the music player")
    async def resume(self, ctx: commands.Context):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed music player!")
        else:
            await ctx.send("The music player is not paused!", silent=True)

    @youtube.command(name="stop", help="Stop the music player")
    async def stop(self, ctx: commands.Context):
        await ctx.invoke(self.leave)

    # TODO: Currently sets bot volume globally; might have unintended
    # effects in other servers; may need to convert volume into a dict
    @youtube.command(name="volume", help="Sets volume of the bot")
    async def volume(self, ctx: commands.Context, volume: int):
        if not check_developer_user(ctx.author.id):
            return await send_message_not_role(ctx, "developer")

        if ctx.voice_client:
            if 0 <= volume <= 100:
                ctx.voice_client.source.volume = float(volume / 100)
                self.volume = float(volume / 100)
                await ctx.send(f"Volume set to {volume}%")
            else:
                await ctx.send("Volume must be between 0 and 100!")
        else:
            await ctx.send("I'm not connected to a voice channel!", silent=True)

    @youtube.command(name="next", help="Play the next song in the queue")
    async def next(self, ctx: commands.Context):
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            # stop playing current song, which SHOULD play next song
            ctx.voice_client.stop()
            await ctx.send(f"Skipping current song!")

    @youtube.command(name="skip", help="Skips current song in the queue")
    async def skip(self, ctx: commands.Context):
        await ctx.invoke(self.next)

    @youtube.command(name="goto", help="Play the song at the queue index")
    async def goto(self, ctx: commands.Context, index: int):
        if ctx.guild.id in self.song_queue and 0 <= index - 1 < len(
            self.song_queue[ctx.guild.id]
        ):
            # move the index tracker to song before the target song
            self.current_song_index[ctx.guild.id] = index - 2
            # stop playing current song, which SHOULD play next song
            ctx.voice_client.stop()
            await ctx.send(f"Playing song at index {index}!", silent=True)
        else:
            await ctx.send("Invalid queue number!", silent=True)

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
            self.current_song_index[ctx.guild.id] = -1
            # note: current song record is not cleared
            await ctx.send("Cleared the playlist!")
        else:
            await ctx.send("No playlist to clear!", silent=True)

    @youtube.command(name="playlist", help="Show the current playlist")
    async def playlist(self, ctx: commands.Context):
        if ctx.guild.id in self.song_queue and len(self.song_queue[ctx.guild.id]) > 0:
            currently_playing_index = self.current_song_index[ctx.guild.id]
            song_list = []
            for index, (url, title) in enumerate(self.song_queue[ctx.guild.id]):
                if index == currently_playing_index:
                    song_list.append(f"**{index + 1}) {title}**")
                else:
                    song_list.append(f"{index + 1}) {title}")

            playlist_string = "\n".join(song_list)
            await ctx.send(f"__Current playlist:__\n{playlist_string}")
        else:
            await ctx.send("The playlist is empty!", silent=True)

    @youtube.command(name="current", description="Displays the current song")
    async def current(self, ctx: commands.Context):
        if ctx.guild.id in self.current_song:
            current_song_url, current_song_title = self.current_song[ctx.guild.id]
            await ctx.send(f"Currently playing: {current_song_title}")
        else:
            await ctx.send("No song is currently playing!", silent=True)

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
            await ctx.send("Invalid queue number!", silent=True)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(YoutubeMusic(bot))
