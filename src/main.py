# AI CHAT BOT
# SCRIPT BY FERDIANWISNUU

import os
import json
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.utils.logger import setup_logger

logger = setup_logger("System")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

load_dotenv(os.path.join(ROOT_DIR, '.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

config_path = os.path.join(BASE_DIR, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['PREFIX'], intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot is active: {bot.user.name}")

async def load_extensions():
    commands_dir = os.path.join(BASE_DIR, 'commands')
    
    for root, dirs, files in os.walk(commands_dir):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, BASE_DIR)
                clean_path = rel_path.replace(os.sep, '.').replace('.py', '')
                actual_path = f"src.{clean_path}" if os.path.basename(os.getcwd()) != "src" else clean_path
                
                try:
                    await bot.load_extension(actual_path)
                    logger.info(f"Merender: {actual_path}")
                except Exception as e:
                    logger.error(f"Tidak Merender {actual_path}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot Is Dead")
