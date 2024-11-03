import pycord
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import psutil
import vcgencmd
import os
import subprocess

load_dotenv(dotenv_path='/enviornmental/.env')

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

print("DISCORD_TOKEN:", TOKEN)  # Should not be None
print("GUILD_ID:", GUILD_ID)    # Should not be None

if GUILD_ID is None:
    raise ValueError("GUILD_ID is not set in the .env file.")

GUILD_ID = int(GUILD_ID)  # Convert after checking 

intents = discord.Intents.default()


bot = commands.Bot(command_prefix='!', intents=intents)

def get_system_stats():
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    try:
        temp_output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        temperature = temp_output.stdout.split('=')[1].split("'")[0]
    except Exception as e:
        temperature = "N/A"
        
    system_stats = (
        f"**CPU Usage**: {cpu_usage}%\n"
        f"**Memory Usage**: {memory_usage}%\n"
        f"**Disk Usage**: {disk_usage}%\n"
        f"**Temperature**: {temperature}°C"
    )
    
    return system_stats

@bot.tree.command(name="PySpy", guild=discord.Object(id=GUILD_ID), description="see what the system stats of the raspberry pi running these bots")
async def pyspy(interaction: discord.Interaction):
    system_stats = get_system_stats()
    await interaction.response.send_message(system_stats)


@bot.event
async def on_ready():
    print(f'bot is online and logged in as {bot.user}')

    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == '/PySpy' or 'pyspy':
        system_stats = get_system_stats()
        await message.channel.send(system_stats)    
        
bot.run(TOKEN)