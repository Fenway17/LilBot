# This example requires the 'message_content' intent.
import os
import discord
from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents) # connection to discord

@client.event
async def on_ready(): # called when the bot is logged in and ready
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message): # called when the bot receives a message
    if message.author == client.user: # check if author is the bot itself
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(BOT_TOKEN)
