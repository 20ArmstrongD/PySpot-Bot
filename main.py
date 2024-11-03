import discord
from discord.ext import commands
from pop import DISCORD_TOKEN, GUILD_ID
from dotenv import load_dotenv
import psutil
import os
import subprocess

# Load environment variables
load_dotenv(dotenv_path='/env/.env')

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
        f"DiscordPI\n"
        f"**CPU Usage**: {cpu_usage}%\n"
        f"**Memory Usage**: {memory_usage}%\n"
        f"**Disk Usage**: {disk_usage}%\n"
        f"**Temperature**: {temperature}°C"
    )
    
    return system_stats

@bot.tree.command(name="pyspy", guild=discord.Object(id=GUILD_ID), description="See what the system stats of the Raspberry Pi running these bots are.")
async def pyspy(interaction: discord.Interaction):
    system_stats = get_system_stats()
    await interaction.response.send_message(system_stats)

@bot.event
async def on_ready():
    print(f'Bot is online and logged in as {bot.user}')
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))  #Register the slash commands
        print("/pyspy slash command registerd")
    except:
        print("unable to register /pyspy slash command")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == '/pyspy' or message.content.lower() == 'pyspy':  # Ensure both '/pyspy' and 'pyspy' are checked
        system_stats = get_system_stats()
        await message.channel.send(system_stats)

bot.run(DISCORD_TOKEN)
