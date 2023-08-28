

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
import discord
from discord.ext import commands, tasks
import random
import asyncio
import datetime
import json
import os

from helpers import checks

class Farm(commands.Cog):
    def __init__(self):
        super().__init__()
        self.value = None
        
    def __init__(self, bot):
        self.bot = bot
        self.potato_farms = {}
        self.grow_potatoes.start()

        self.load_data()  # Load data from JSON file

    def save_data(self):
        with open("potatofarm.json", "w") as file:
            json.dump(self.potato_farms, file)

    def load_data(self):
        if os.path.exists("potatofarm.json"):
            with open("potatofarm.json", "r") as file:
                self.potato_farms = json.load(file)

    @tasks.loop(minutes=5)  # Simulate time passing
    async def grow_potatoes(self):
        for user_id in self.potato_farms:
            self.potato_farms[user_id]['potatoes'] += random.randint(1, 5)

    @commands.command()
    async def plant(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.potato_farms:
            self.potato_farms[user_id] = {'potatoes': 10}
            self.save_data()  # Save data to JSON file
            await ctx.send("You've started your potato farm!")
        else:
            await ctx.send("You already have a potato farm.")

    @commands.command()
    async def harvest(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.potato_farms:
            potatoes = self.potato_farms[user_id]['potatoes']
            if potatoes >= 5:
                reward = random.randint(5, 10)
                self.potato_farms[user_id]['potatoes'] -= 5
                self.save_data()  # Save data to JSON file
                await ctx.send(f"You harvested 5 potatoes and gained {reward} rewards.")
            else:
                await ctx.send("Your potatoes are not ripe yet.")
        else:
            await ctx.send("You don't have a potato farm. Use the `plant` command to start one.")

    @commands.command()
    async def farm(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.potato_farms:
            potatoes = self.potato_farms[user_id]['potatoes']
            await ctx.send(f"Your potato farm has {potatoes} potatoes.")
        else:
            await ctx.send("You don't have a potato farm. Use the `plant` command to start one.")

    @commands.command()
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.potato_farms:
            farm = self.potato_farms[user_id]
            last_claim = farm.get('last_claim')
            if last_claim is None or (datetime.datetime.now() - datetime.datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S.%f")).days >= 1:
                bonus = random.randint(10, 20)
                farm['potatoes'] += bonus
                farm['last_claim'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                self.save_data()  # Save data to JSON file
                await ctx.send(f"You claimed your daily bonus of {bonus} potatoes!")
            else:
                remaining_time = (datetime.datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S.%f") + datetime.timedelta(days=1)) - datetime.datetime.now()
                await ctx.send(f"You've already claimed your daily bonus. Try again in {remaining_time}.")
        else:
            await ctx.send("You don't have a potato farm. Use the `plant` command to start one.")

    @commands.command()
    async def leaderboard(self, ctx):
        sorted_farms = sorted(self.potato_farms.items(), key=lambda x: x[1]['potatoes'], reverse=True)
        leaderboard = "\n".join([f"{i+1}. <@{user_id}>: {farm['potatoes']} potatoes" for i, (user_id, farm) in enumerate(sorted_farms)])
        await ctx.send(f"Potato Farm Leaderboard:\n{leaderboard}")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    

async def setup(bot):
    await bot.add_cog(Farm(bot))
