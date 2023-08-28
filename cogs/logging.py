import discord
from discord.ext import commands
import math
import datetime
from discord.ext.commands import Context


class Logging(commands.Cog, name="logging"):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    channel = self.bot.get_channel(1145295668697628712)
    embed = discord.Embed(
        title=f"Message deleted in <#{message.channel.id}>",
        description=f"{message.content}\n\nMessage ID: {message.id}",
        color=0xFF0000,
        timestamp=datetime.datetime.now())
    embed.set_author(name=message.author.name, icon_url=message.author.avatar)
    embed.set_footer(text=f'User ID: {message.author.id}')
    # await channel.send(f'message: {message.content} by {message.author} was deleted in #{message.channel}')
    await channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.content != after.content:
      channel = self.bot.get_channel(1145295668697628712)
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
