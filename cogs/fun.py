

import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
import asyncio
import os
import json
import io
from PIL import Image

from helpers import checks

huggingfacekey = os.environ.get('huggingfacekey')

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0x9C84EF)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.avatar.url
        )

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x9C84EF
        else:
            result_embed.description = (
                f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            )
            result_embed.colour = 0xE02B2B
        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    @checks.not_blacklisted()
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    @checks.not_blacklisted()
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0x9C84EF)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0x9C84EF,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    async def fetch_cat_picture(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as response:
                data = await response.json()
                if data:
                    return data[0]["url"]
                return None
  
    @commands.hybrid_command(
        name="cat",
        description="Get a random picture of a cat.",
    )
    @checks.not_blacklisted()
    async def cat(self, context: commands.Context):
        cat_url = await self.fetch_cat_picture()

        if cat_url:
            embed = discord.Embed(
                title="Random Cat Picture",
                color=discord.Color.orange(),
            )
            embed.set_image(url=cat_url)
            await context.send(embed=embed)
        else:
            await context.send("Failed to fetch a cat picture. Please try again.")

    @commands.command(
        name="anime",
        description="Get a random anime image and rate it.",
    )
    async def anime(self, ctx: commands.Context) -> None:
        response = requests.get('https://api.catboys.com/img')
        if response.status_code == 200:
            data = response.json()
            image_url = data['url']
            artist = data['artist']

            embed = discord.Embed(title=f"Artist: {artist}", url=image_url)
            embed.set_image(url=image_url)

            if artist == "unknown":
                embed.description = "If you're the owner of this image, you might want to try to contact https://catboys.com/api (The API we use to pull data)"

            anime_msg = await ctx.send(embed=embed)
            await anime_msg.add_reaction('👍')
            await anime_msg.add_reaction('👎')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['👍', '👎']

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=5.0, check=check)
                rating = 1 if reaction.emoji == '👍' else -1

                if str(anime_msg.id) not in anime_ratings:
                    anime_ratings[str(anime_msg.id)] = {'total': 0, 'count': 0}

                anime_ratings[str(anime_msg.id)]['total'] += rating
                anime_ratings[str(anime_msg.id)]['count'] += 1

                average_rating = anime_ratings[str(anime_msg.id)]['total'] / anime_ratings[str(anime_msg.id)]['count']

                with open('anime_ratings.json', 'w') as file:
                    json.dump(anime_ratings, file)

                embed.set_footer(text=f"Average Rating: {average_rating:.2f}")
                await anime_msg.edit(embed=embed)

            except asyncio.TimeoutError:
                pass

        else:
            await ctx.send("An error occurred while fetching anime data.")

async def setup(bot):
    await bot.add_cog(Fun(bot))
