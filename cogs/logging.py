import discord
from discord.ext import commands
import datetime
from discord.ext.commands import Context
from helpers import checks
from discord import app_commands

class Logging(commands.Cog, name="logging"):

    def __init__(self, bot):
        self.bot = bot
        self.logging_channels = {}

    @commands.hybrid_command(
        name="setloggingchannel",
        description="Sets the logging channel for the server."
    )
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        channel="The channel you want the logging channel to be",
    )
    async def setloggingchannel(
        self, context: Context, channel: discord.TextChannel = None
    ) -> None:
        """
        Set the logging channel.
        :param context: The hybrid command context.
        :param channel: The channel you want the logging channel to be. Default is "None".
        """
        if channel:
            self.logging_channels[context.guild.id] = channel.id
            embed=discord.Embed(
                description=f"Set the logging channel to <#{channel.id}>.",
                color=0x008000
            )
            await Context.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel_id = self.logging_channels.get(message.guild.id)
        if channel_id is not None:
            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(
                title=f"Message deleted in <#{message.channel.id}>",
                description=f"{message.content}\n\nMessage ID: {message.id}",
                color=0xFF0000,
                timestamp=datetime.datetime.now())
            embed.set_author(name=message.author.name, icon_url=message.author.avatar)
            embed.set_footer(text=f'User ID: {message.author.id}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            channel_id = self.logging_channels.get(after.guild.id)
            if channel_id is not None:
                channel = self.bot.get_channel(channel_id)
                embed = discord.Embed(
                    title=f"Message edited in <#{after.channel.id}>",
                    description=
                    f"**Before:** {before.content}\n**After:** {after.content}\n\nMessage ID: {after.id}",
                    color=0x5865F2,
                    timestamp=datetime.datetime.now())

                embed.set_author(name=after.author.name, icon_url=after.author.avatar)
                embed.set_footer(text=f"User ID: {after.author.id}")

                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logging(bot))
