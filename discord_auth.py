'''

    [discord_auth.py]
    import as discord

    connects to discord

    has no functions currently but probably wanna add
    something like discord.put

'''


# authorization for discord =======================================================================================================

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents = intents)

