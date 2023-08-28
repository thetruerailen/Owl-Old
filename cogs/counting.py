import discord
from discord.ext import commands
import math

class Counting(commands.Cog, name="counting"):
    def __init__(self, bot):
        self.bot = bot
        self.count = self.load_count()  # Load the count from the file
        self.current_user = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == 1145273832270221392:
            if message.author.id == 1144589654570573924:
                return
            
            try:
                content = message.content
                if content.isnumeric() or self.is_valid_expression(content):
                    expr_result = self.evaluate_expression(content)
                    if expr_result == self.count + 1:
                        self.count = expr_result
                        self.current_user = message.author
                        await self.save_count()
                        await self.add_reaction(message, "\U00002705")  # Add a white check mark
                    else:
                        await message.delete()  # Delete the message if it breaks the sequence
                else:
                    await message.delete()  # Delete the message if it's not a valid number or expression
            except (ValueError, SyntaxError, NameError, TypeError, ZeroDivisionError):
                await message.delete()  # Delete messages with invalid input
            

    def is_valid_expression(self, expr):
        try:
            eval(expr)
            return True
        except:
            return False

    def evaluate_expression(self, expr):
        return eval(expr)

    async def send_embed(self, description, color, channel):
        embed = discord.Embed(description=description, color=color)
        await channel.send(embed=embed)

    async def add_reaction(self, message, emoji):
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    async def save_count(self):
        with open("counting_data.txt", "w") as file:
            file.write(str(self.count))  # Save the current count to the file

    def load_count(self):
        try:
            with open("counting_data.txt", "r") as file:
                return int(file.read())  # Load the count from the file
        except FileNotFoundError:
            return 0  # If the file doesn't exist, start counting from 0


async def setup(bot):
    await bot.add_cog(Counting(bot))
