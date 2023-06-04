import discord
from discord.ext import commands


class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member):
    #     guild = member.guild
    #     if guild.system_channel is not None:
    #         await guild.system_channel.send(member.mention)
    #         embed=discord.Embed(title=f"Welcome to **{guild.name}**!",
    #                             description=f'Welcome {member.mention}! I hope you will have fun here!',
    #                             color=0x00ff00)
    #         await guild.system_channel.send(embed=embed)

        
    



async def setup(bot:commands.Bot):
    await bot.add_cog(Greeting(bot))
