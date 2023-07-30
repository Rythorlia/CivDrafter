import discord
import os
import random
import typing
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() # load our .env file to access our secrets

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='/', intents=intents)
    
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# define our commands for the user to enter
@bot.command(pass_context=True, name='draft')
async def draft_civs(ctx, game_type:str, number_of_civs_draft:int=3):
    await ctx.send(game_type)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  for guild in client.guilds:
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$test'):
    await message.channel.send('Bot is alive and well')

bot.run(os.getenv('DISCORD_TOKEN')) # secret token for the CivDrafter bot stored in a .env file
