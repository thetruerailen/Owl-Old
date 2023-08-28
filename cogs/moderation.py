
from datetime import timedelta
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Union
import openai

from helpers import checks, db_manager


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kick",
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should be kicked.",
        reason="The reason why the user should be kicked.",
    )
    async def kick(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Kick a user out of the server.

        :param context: The hybrid command context.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="User has administrator permissions.", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=0x9C84EF,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)






    @commands.hybrid_command(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should have a new nickname.",
        nickname="The new nickname that should be set.",
    )
    async def nick(
        self, context: Context, user: discord.User, *, nickname: str = None
    ) -> None:
        """
        Change the nickname of a user on a server.

        :param context: The hybrid command context.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x9C84EF,
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)






    @commands.hybrid_command(
        name="ban",
        description="Bans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should be banned.",
        reason="The reason why the user should be banned.",
    )
    async def ban(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Bans a user from the server.

        :param context: The hybrid command context.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description="Nuh uh, user has administrator permissions.", color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                try:
                    await member.send(
                        f"You were banned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    pass  # Couldn't send a message in the private messages of the user

                await member.ban(reason=reason)
                embed = discord.Embed(
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=0x9C84EF,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description=f"An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.\nError: `{e}`",
                color=0xE02B2B,
            )
            await context.send(embed=embed)





    @commands.hybrid_command(
        name="unban",
        description="Unbans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should be unbanned",
        reason="The reason why the user should be unbanned"
    )
    async def unban(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Unbans a user from the server.

        :param context: The hybrid command context.
        :param user: The user that should be unbanned from the server.
        :param reason: The reason for the unban. Default is "Not specified".
        """
        try:
            bans = await context.guild.bans()
            bans_list = await bans.flatten()  # Convert the async generator to a list

            banned_entry = None
            for entry in bans_list:
                if entry.user.id == user.id:
                    banned_entry = entry
                    break
                
            if banned_entry is not None:
                await context.guild.unban(banned_entry.user, reason=reason)

                embed = discord.Embed(
                    description=f"**{banned_entry.user}** was unbanned by **{context.author}**!",
                    color=0x9C84EF,
                )
                embed.add_field(name="Reason:", value=reason)
                await context.send(embed=embed)

                try:
                    await banned_entry.user.send(
                        f"You were unbanned by **{context.author}** from **{context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    pass
            else:
                embed = discord.Embed(
                    title="Error!",
                    description="The specified user is not banned.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description=f"An error occurred while trying to unban the user. Are you sure the user is banned?\nError: `{e}`",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            print(f"An error occurred during unban: {e}")








    @commands.hybrid_group(
        name="warn",
        description="Manage warnings of a user on a server.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warn(self, context: Context) -> None:
        """
        Manage warnings of a user on a server.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)






    @warn.command(
        name="add",
        description="Adds a warning to a user in the server.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should be warned.",
        reason="The reason why the user should be warned.",
    )
    async def warning_add(
        self, context: Context, user: discord.User, *, reason: str = "Not specified"
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await db_manager.add_warn(
            user.id, context.guild.id, context.author.id, reason
        )
        embed = discord.Embed(
            description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
            color=0x9C84EF,
        )
        embed.add_field(name="Reason:", value=reason)
        await context.send(embed=embed)
        try:
            await member.send(
                f"You were warned by **{context.author}** in **{context.guild.name}**!\nReason: {reason}"
            )
        except:
            # Couldn't send a message in the private messages of the user
            await context.send(
                f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}"
            )







    @warn.command(
        name="remove",
        description="Removes a warning from a user in the server.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(
        user="The user that should get their warning removed.",
        warn_id="The ID of the warning that should be removed.",
    )
    async def warning_remove(
        self, context: Context, user: discord.User, warn_id: int
    ) -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should get their warning removed.
        :param warn_id: The ID of the warning that should be removed.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(
            user.id
        )
        total = await db_manager.remove_warn(warn_id, user.id, context.guild.id)
        embed = discord.Embed(
            description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
            color=0x9C84EF,
        )
        await context.send(embed=embed)







    @warn.command(
        name="list",
        description="Shows the warnings of a user in the server.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def warning_list(self, context: Context, user: discord.User):
        """
        Shows the warnings of a user in the server.

        :param context: The hybrid command context.
        :param user: The user you want to get the warnings of.
        """
        warnings_list = await db_manager.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(title=f"Warnings of {user}", color=0x9C84EF)
        description = ""
        if len(warnings_list) == 0:
            description = "This user has no warnings."
        else:
            for warning in warnings_list:
                description += f"• Warned by <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - Warn ID #{warning[5]}\n"
        embed.description = description
        await context.send(embed=embed)






    @commands.hybrid_command(
        name="purge",
        description="Delete a number of messages.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(amount="The amount of messages that should be deleted.")
    async def purge(self, context: Context, amount: int) -> None:
        """
        Delete a number of messages.

        :param context: The hybrid command context.
        :param amount: The number of messages that should be deleted.
        """
        await context.send(
            "Deleting messages..."
        )  # Bit of a hacky way to make sure the bot responds to the interaction and doens't get a "Unknown Interaction" response
        purged_messages = await context.channel.purge(limit=amount + 2)
        embed = discord.Embed(
            description=f"**{context.author}** cleared **{len(purged_messages)-2}** messages!",
            color=0x9C84EF,
        )
        await context.channel.send(embed=embed)






    @commands.hybrid_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user_id="The user ID that should be banned.",
        reason="The reason why the user should be banned.",
    )
    async def hackban(
        self, context: Context, user_id: str, *, reason: str = "Not specified"
    ) -> None:
        """
        Bans a user without the user having to be in the server.

        :param context: The hybrid command context.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(
                int(user_id)
            )
            embed = discord.Embed(
                description=f"**{user}** (ID: {user_id}) was banned by **{context.author}**!",
                color=0x9C84EF,
            )
            embed.add_field(name="Reason:", value=reason)
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description="An error occurred while trying to ban the user. Make sure that the ID is an existing ID that belongs to a user.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)








    @commands.hybrid_command(
        name="mute",
        description="Mutes a user for a specified duration.",
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should be muted.",
        duration="The duration of the mute (e.g., '1s' for 1 second, '1m' for 1 minute, etc.).",
        reason="The reason for the mute.",
    )
    async def mute(
        self, context: Context, user: discord.User, duration: str, *, reason: str = "Not specified"
    ) -> None:
        """
        Mutes a user for a specified duration.

        :param context: The hybrid command context.
        :param user: The user that should be muted.
        :param duration: The duration of the mute (e.g., '1s' for 1 second, '1m' for 1 minute, etc.).
        :param reason: The reason for the mute. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        
        # Check if the user already has the "Muted" role
        mute_role = discord.utils.get(context.guild.roles, name="Muted")
        if mute_role in member.roles:
            embed = discord.Embed(
                description=f"**{member}** is already muted.",
                color=0xFF0000
            )
            await context.send(embed=embed)
            return
        
        # Create the "Muted" role if it doesn't exist
        if not mute_role:
            mute_role = await context.guild.create_role(name="Muted")
            for channel in context.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)
        
        await member.add_roles(mute_role, reason=reason)
        
        time_unit = duration[-1]
        time_value = int(duration[:-1])
        if time_unit == 's':
            mute_duration = timedelta(seconds=time_value)
        elif time_unit == 'm':
            mute_duration = timedelta(minutes=time_value)
        elif time_unit == 'h':
            mute_duration = timedelta(hours=time_value)
        elif time_unit == 'd':
            mute_duration = timedelta(days=time_value)
        elif time_unit == 'w':
            mute_duration = timedelta(weeks=time_value)
        else:
            raise commands.BadArgument("Invalid time unit. Use 's', 'm', 'h', 'd', or 'w'.")
        

        embed = discord.Embed(
            description=f"**{member}** was muted by **{context.author}** for {duration}",
            color=0x9C84EF,
        )
        embed.add_field(name="Reason:", value=reason)
        await context.send(embed=embed)

        try:
            await member.send(
                f"You were muted by **{context.author}** in **{context.guild.name}** for {duration}!\nReason: {reason}"
            )
        except:
            pass
        
        await asyncio.sleep(mute_duration.total_seconds())
        await member.remove_roles(mute_role, reason="Mute duration ended")
        await member.send(f"Your mute by **{context.author}** in **{context.guild.name}** expired.")








    @commands.hybrid_command(
        name="unmute",
        description="Unmute a muted user.",
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(
        user="The user that should be unmuted.",
        reason="The reason for the mute.",
    )

    async def unmute(
        self, context: Context, user: discord.User, reason: str = "Not specified"
    ) -> None:
        
        """
        Mutes a user for a specified duration.

        :param context: The hybrid command context.
        :param user: The user that should be muted.
        :param reason: The reason for the mute. Default is "Not specified".
        """

        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        mute_role = discord.utils.get(context.guild.roles, name="Muted")
        if mute_role in member.roles:
            embed = discord.Embed(
                description=f"**{member}** was unmuted",
                color=0x9C84EF
            )
            await context.send(embed=embed)
            await member.remove_roles(mute_role, reason="Manual Unmute")
            await member.send(
                f"You were unmuted by **{context.author}** in **{context.guild.name}**!\nReason: {reason}"
            )
            return
        embed = discord.Embed(
            description=f"**{member}** is not muted",color=0xFF0000
        )
        await context.send(embed=embed)











    @commands.hybrid_command(
    name="slowmode",
    description="Sets the slowmode for a channel",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def slowmode(
        self, context: Context, args: commands.Greedy[Union[discord.TextChannel, int]]
    ) -> None:
        """
        Sets the slowmode for a channel.

        :param context: The hybrid command context.
        :param args: A list of arguments, containing the channel and seconds.
        """
        if len(args) == 2:
            channel = args[0]
            time = args[1]
        else:
            channel = context.channel
            time = args[0]

        if time > 21600:
            embed = discord.Embed(
                description="Slowmode time cannot be higher than 21600 seconds (6 hours).",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        if isinstance(channel, discord.TextChannel):
            await channel.edit(slowmode_delay=time)
            embed = discord.Embed(
                description=f"Slowmode for {channel.mention} set to {time} seconds.",
                color=0x9C84EF,
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(  
                description="Invalid channel provided.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
