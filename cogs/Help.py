import discord
from discord.ext import commands
from discord import Interaction
from discord import app_commands
from discord.ui import Select


class Help(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    # New help command using the select view
    @app_commands.command(name='help', description='lists all available commands')
    async def help(self, interaction:Interaction):
        from misc.load import admin_help, fun_help, misc_help, phasmo_help, music_help, rpg_help
        select = Select(
            placeholder='Select a category',
            options=[
                discord.SelectOption(label='Admin', value='admin', emoji='🛡️'),
                discord.SelectOption(label='Fun', value='fun', emoji='🎲'),
                discord.SelectOption(label='Misc', value='misc', emoji='🔨'),
                discord.SelectOption(label='Phasmophobia', value='phasmo', emoji='👻'),
                discord.SelectOption(label='Music', value='music', emoji='🎵'),
                discord.SelectOption(label='RPG', value='rpg', emoji='⚔️')
            ],
            min_values=1,
            max_values=1            
        )

        embed = discord.Embed(title='📖 A list with all available commands 📖', description='\u200b', color=discord.Color.blue())
        embed.add_field(name='Please choose a category down below!', value='\u200b', inline=True)


        async def a_callback(interaction:Interaction):
            if select.values[0] == 'admin':
                await interaction.response.edit_message(embed=discord.Embed(title='🛡️ Admin commands 🛡️', description=str(admin_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))
            elif select.values[0] == 'fun':
                await interaction.response.edit_message(embed=discord.Embed(title='🎲 Fun commands 🎮', description=str(fun_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))
            elif select.values[0] == 'misc':
                await interaction.response.edit_message(embed=discord.Embed(title='🔨 miscellaneous commands 🔨', description=str(misc_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))
            elif select.values[0] == 'phasmo':
                await interaction.response.edit_message(embed=discord.Embed(title='👻 Phasmophobia commands 👻', description=str(phasmo_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))
            elif select.values[0] == 'music':
                await interaction.response.edit_message(embed=discord.Embed(title='🎵 Music commands 🎵', description=str(music_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))
            elif select.values[0] == 'rpg':
                await interaction.response.edit_message(embed=discord.Embed(title='⚔️ RPG commands 🏹', description=str(rpg_help).replace('[', '').replace(']', '').replace("'", '').replace(",", '\n'), color=discord.Color.blue()))


        select.callback = a_callback
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot:commands.Bot):
    await bot.add_cog(Help(bot))