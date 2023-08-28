import aiohttp
import discord
from discord.ext import commands
import openai  # Add this import for the openai module
import os

from helpers import checks

class AI(commands.Cog, name="AI"):
    def __init__(self, bot):
        self.bot = bot
        self.openai.api_key = os.environ['API Key']

    @commands.hybrid_command(
        name="chatgpt",
        description="Chat with the bot using GPT-3.5.",
    )
    async def chatgpt(self, context: commands.Context, *, message: str):
        openai.api_key = self.openai_api_key  # Set the API key
        
        conversation = [
            {"role": "user", "content": message}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        
        bot_reply = response.choices[0].message["content"]
        
        await context.send(bot_reply)
