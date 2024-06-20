import re
from typing import Dict, List
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import utils.responses as responses

# Spotify credentials
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="SPOTIFY_CLIENT_ID", client_secret="SPOTIFY_CLIENT_SECRET"
    )
)

YOUTUBE_URL_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"
)


# searches for the metadata through spotify and converts it into a youtube url to play music
class SpotifyMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    # for commands.hybrid_group, Group.invoke_without_command is auto set to True
    @commands.hybrid_group(
        name="spotify", description="Youtube player related commands"
    )
    async def spotify(self, ctx: commands.Context):
        await ctx.send(responses.USER_NO_SUBCOMMANDS, silent=True, delete_after=5)

    # main command logic of adding youtube videos to queue
    @spotify.command(name="play", help="Play a song from Spotify")
    @app_commands.describe(url="Provide Spotify URL to song")
    async def play_spotify(self, ctx: commands.Context, *, url: str = None):
        # extract the track ID from the Spotify URL
        track_id = url.split("/")[-1].split("?")[0]
        if not track_id:
            return await ctx.send(
                responses.USER_INVALID_INPUT, silent=True, delete_after=10
            )

        # get track details from Spotify
        track = sp.track(track_id)
        if not track:
            return await ctx.send(
                responses.SPOTIFY_TRACK_NOT_FOUND, silent=True, delete_after=10
            )
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        search_query = f"{track_name} {artist_name}"

        # send search query to youtube music player cog
        print("sending command to youtube_player")
        play_command = self.bot.get_command("youtube play")
        await ctx.invoke(play_command, search_query)


async def setup(bot: commands.Bot):  # required for adding cog to the bot
    await bot.add_cog(SpotifyMusic(bot))
