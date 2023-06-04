import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Kick command - kicks members from a Guild
    @app_commands.command(name='kick', description='kicks a member')
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: Interaction, member:discord.Member, *, reason:str = None):
        await member.kick(reason=reason)
        embed = discord.Embed(title='Member Kicked', description=f'{member.name} has been kicked from the server.\nReason: {reason}', color=0x00ff00)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url) 

        await interaction.response.send_message(embed=embed)

        print(f'{interaction.user.name}#{interaction.user.discriminator} kicked {member.name}#{member.discriminator} from {interaction.guild.name} for {reason}')
        

    # Ban command - bans members from a Guild
    @app_commands.command(name='ban', description='bans a member')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: Interaction, member:discord.Member, *, reason:str = None):
        await member.ban(reason=reason)
        embed = discord.Embed(title='Member Banned', description=f'{member.name} has been banned from the server.\nReason: {reason}', color=0x00ff00)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f'{interaction.user.name}#{interaction.user.discriminator} banned {member.name}#{member.discriminator} from {interaction.guild.name} for {reason}')
    
    # Unban command - unbans members from a Guild
    @app_commands.command(name='unban', description='unbans a member')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: Interaction, *, member:discord.User):
        banned_users = await interaction.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                embed = discord.Embed(title='Member Unbanned', description=f'{user.name}#{user.discriminator} has been unbanned from the server.', color=0x00ff00)
                embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                return
            else:
                await interaction.response.send_message(f'{member} was not found')
                return

        print(f'{interaction.user.name}#{interaction.user.discriminator} unbanned {member.name}#{member.discriminator} from {interaction.guild.name}')
    
    # Clear command - clears messages from a channel

    @app_commands.command(name='clear', description='clears messages from a channel')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: Interaction, amount: int):
        await interaction.channel.purge(limit=amount, before=interaction.created_at)
        embed = discord.Embed(title='Messages Cleared', description=f'{amount} messages have been cleared from the channel.', color=0x00ff00)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f'{interaction.user.name}#{interaction.user.discriminator} cleared {amount} messages from {interaction.channel.name} in {interaction.guild.name}')


    # Warn command - warns a member

    @app_commands.command(name='warn', description='warns a member')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: Interaction, member:discord.Member, *, reason:str=None):
        embed = discord.Embed(title='Warn', description=f'{member.mention} has been warned for `**{reason}**`', color=discord.Color.red())
        await interaction.response.send_message(member.mention, embed=embed)

        print(f'{interaction.user.name}#{interaction.user.discriminator} warned {member.name}#{member.discriminator} in {interaction.guild.name} for {reason}')
    

    # slowmode command - sets the slowmode of a channel

    @app_commands.command(name='slowmode', description='sets the slowmode of a channel')
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title='Slowmode', description=f'Slowmode has been set to {seconds} seconds', color=0x00ff00)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url) 
        await interaction.response.send_message(embed=embed)

        print(f'{interaction.user.name}#{interaction.user.discriminator} set the slowmode of {interaction.channel.name} to {seconds} seconds in {interaction.guild.name}')



async def setup(bot:commands.Bot):
    await bot.add_cog(Admin(bot))