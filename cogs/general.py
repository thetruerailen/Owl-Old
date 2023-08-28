

import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import requests
from bs4 import BeautifulSoup

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0x9C84EF
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="info",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def info(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="bot made by nils",
            color=0x9C84EF,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="<@1141250816120999998>", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF,
        )
        await context.send(embed=embed)

    #   @commands.hybrid_command(
    #       name="invite",
    #       description="Get the invite link of the bot to be able to invite it.",
    #   )
    #@checks.not_blacklisted()
    #async def invite(self, context: Context) -> None:
    #    """
    #    Get the invite link of the bot to be able to invite it.
#
    #    :param context: The hybrid command context.
    #    """
    #    embed = discord.Embed(
    #        description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={self.bot.config['application_id']}&scope=bot+applications.commands&permissions={self.bot.config['permissions']}).",
    #        color=0xD75BF4,
    #    )
    #    try:
    #        # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
    #        await context.author.send(embed=embed)
    #        await context.send("I sent you a private message!")
    #    except discord.Forbidden:
    #        await context.send(embed=embed)
#
    #@commands.hybrid_command(
    #    name="server",
    #    description="Get the invite link of the discord server of the bot for some support.",
    #)
    #@checks.not_blacklisted()
    #async def server(self, context: Context) -> None:
    #    """
    #    Get the invite link of the discord server of the bot for some support.
#
    #    :param context: The hybrid command context.
    #    """
    #    embed = discord.Embed(
    #        description=f"Join the support server for the bot by clicking [here](https://discord.gg/eNcnT4hDZv).",
    #        color=0xD75BF4,
    #    )
    #    try:
    #        await context.author.send(embed=embed)
    #        await context.send("I sent you a private message!")
    #    except discord.Forbidden:
    #        await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def eight_ball(self, context: commands.Context, *, question: str) -> None:
        response = requests.get('https://api.catboys.com/8ball')
        if response.status_code == 200:
            data = response.json()
            saying = data['response']
            image_url = data['url']

            embed = discord.Embed(title="Magic 8-Ball", description=f"Response: {saying}")
            embed.set_image(url=image_url)

            await context.channel.send(embed=embed)
        else:
            await context.channel.send("An error occurred while fetching 8ball data.")

    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
            ) as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript"
                    )  # For some reason the returned content is of type JavaScript
                    embed = discord.Embed(
                        title="Bitcoin price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=0x9C84EF,
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="bing",
        description="Perform a Bing search and display the results.",
    )
    async def bing(self, context: commands.Context, *, query):
        # Construct the Bing search URL
        search_url = f"https://www.bing.com/search?q={query}"

        try:
            # Send a request to Bing and get the HTML content
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract search results
            results = []
            for result in soup.select(".b_algo"):
                title = result.select_one("h2").get_text()
                link = result.select_one("a")["href"]
                snippet = result.select_one(".b_caption p")
                snippet_text = snippet.get_text() if snippet else "No snippet available"
                results.append(f"**{title}**\n{link}\n{snippet_text}")

            # Send the search results to the Discord channel
            if results:
                await context.send("\n\n".join(results))
            else:
                await context.send("No results found.")

        except requests.RequestException as e:
            await context.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(General(bot))
