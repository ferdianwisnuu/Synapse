import discord
from discord.ext import commands
from src.services.ai_service import AIService

class AICommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_service = AIService()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        is_mentioned = self.bot.user.mentioned_in(message)
        is_reply_to_bot = False

        if message.reference and message.reference.cached_message:
            referenced_msg = message.reference.cached_message
            if referenced_msg.author == self.bot.user:
                is_reply_to_bot = True
        elif message.reference and not message.reference.cached_message:
            try:
                referenced_msg = await message.channel.fetch_message(message.reference.message_id)
                if referenced_msg.author == self.bot.user:
                    is_reply_to_bot = True
            except discord.HTTPException:
                pass

        if is_mentioned or is_reply_to_bot:
            clean_content = message.content
            if is_mentioned:
                clean_content = clean_content.replace(f'<@!{self.bot.user.id}>', '').replace(f'<@{self.bot.user.id}>', '')
            clean_content = clean_content.strip()

            if not clean_content:
                return

            if is_mentioned:
                self.ai_service.clear_user_memory(message.author.id)

            async with message.channel.typing():
                try:
                    answer = await self.ai_service.generate_response(
                        user_id=message.author.id,
                        username=message.author.name,
                        channel_name=message.channel.name,
                        user_message=clean_content
                    )
                    
                    if len(answer) > 2000:
                        for i in range(0, len(answer), 2000):
                            await message.reply(answer[i:i+2000])
                    else:
                        await message.reply(answer)
                except Exception:
                    await message.reply("Terjadi Kesalahan")

    @commands.command(name='clear')
    async def clear_memory(self, ctx):
        success = self.ai_service.clear_user_memory(ctx.author.id)
        if success:
            await ctx.send("Conversation memory cleared!")
        else:
            await ctx.send("No conversation memory!")

async def setup(bot):
    await bot.add_cog(AICommand(bot))