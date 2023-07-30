import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


client.run(os.getenv("DISCORD_TOKEN")) # secret token for the CivDrafter bot stored in a .env file
