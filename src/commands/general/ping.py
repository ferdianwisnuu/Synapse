import discord
from discord.ext import commands
import time

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        
        start_time = time.time()
        message = await ctx.send("Checking...")
        api_latency = round((time.time() - start_time) * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot Latency: {bot_latency}ms\nAPI Latency: {api_latency}ms",
            color=discord.Color.blue()
        )
        
        await message.edit(content=None, embed=embed)

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
