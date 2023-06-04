import discord
from discord.ext import commands
from discord import Interaction
from discord import app_commands

# Import the lists for the 8ball command
from misc.load import eightballresponses
from misc.load import eightballnoquestion

# Import the required modules and lists for the commands
from random import choice


class Fun(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    # 8Ball command, ask a question and it will give a random answer from a set list

    @app_commands.command(name='8ball', description='Ask a question!')
    async def eightball(self, interaction: Interaction, question:str='null'):
        if question == 'null':
            embed = discord.Embed(title="You didn't ask anything!", description=f'{choice(eightballnoquestion)}', color=discord.Color.blue())
            embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="\U0001F3B1 8ball \U0001F3B1", color=discord.Color.blue())
            embed.add_field(name='Question', value=f'{question}', inline=False)
            embed.add_field(name='Answer', value=f'{choice(eightballresponses)}', inline=False)
            embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the 8ball command in {interaction.guild.name} with the question {question}")

    # Choices! Struggle with chosing what to do? Let the bot help you with that!

    @app_commands.command(name='choice', description="Let the bot choose between 2 things!")
    async def choose(self, interaction: Interaction, item1: str , item2: str):
        answer = choice([item1,item2])
        embed = discord.Embed(title='Choice', color=discord.Color.blue())
        embed.add_field(name=f'Choose between {item1} and {item2}', value='\u200b', inline=False)
        embed.add_field(name=f'Answer: {answer}', value='\u200b', inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url) 
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the choice command in {interaction.guild.name} with the choices {item1} and {item2}")

    # Coinflip command, flip a coin and get heads or tails!

    @app_commands.command(name='coinflip', description='Flip a coin!')
    async def coinflip(self, interaction: Interaction):
        answer = choice(['heads','tails'])
        embed = discord.Embed(title=f'\U0001fa99 Flipping the coin \U0001fa99', color=discord.Color.blue())
        embed.add_field(name=f'It landed on {answer}!', value='\u200b', inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the coinflip command in {interaction.guild.name}")

    # Ping command, check the bots ping!

    @app_commands.command(name='ping', description='Check the bots ping!')
    async def ping(self, interaction: Interaction):
        embed = discord.Embed(title=f'My ping is : {round(self.bot.latency * 1000)}ms', color=discord.Color.blue())
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the ping command in {interaction.guild.name}")

    # Say command, make the bot say something!

    @app_commands.command(name='say', description='Make the bot say something!')
    async def say(self, interaction: Interaction, *, message:str):
        await interaction.response.send_message(message)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the say command in {interaction.guild.name} with the message {message}")
    
    # Userinfo command, get information about a user!

    @app_commands.command(name='userinfo', description='Get information about a user!')
    async def userinfo(self, interaction: Interaction, user: discord.Member = None):
        if user == None:
            user = interaction.user
            
        created_at = user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
        joined_at = user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
        embed = discord.Embed(title=f'Userinfo for {user}', description=f'Here is the information about {user}', color=discord.Color.blue())
        embed.set_image(url=user.display_avatar.url)
        embed.add_field(name='Name', value=user.name, inline=False)
        embed.add_field(name='ID', value=user.id, inline=False)
        embed.add_field(name='Status', value=user.status, inline=False)
        embed.add_field(name='Account created at', value=created_at, inline=False)
        embed.add_field(name='Joined at', value=joined_at, inline=False)          
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)  
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the userinfo command in {interaction.guild.name} with the user {user}")

    # Serverinfo command, get information about the server!

    @app_commands.command(name='serverinfo', description='Get information about the server!')
    async def serverinfo(self, interaction: Interaction):

        if interaction.guild.icon == None:
            icon = 'https://cdn.discordapp.com/embed/avatars/0.png'
        else:
            icon = interaction.guild.icon.url
        created_at = interaction.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
        embed = discord.Embed(title=f'Server info for {interaction.guild}', description=f'Here is the information about {interaction.guild}', color=discord.Color.blue())
        embed.add_field(name='Name', value=interaction.guild.name, inline=False)
        embed.add_field(name='ID', value=interaction.guild.id, inline=False)
        embed.add_field(name='Owner', value=interaction.guild.owner, inline=False)
        embed.add_field(name='Region', value=interaction.guild.region, inline=False)
        embed.add_field(name='Members', value=interaction.guild.member_count, inline=False)
        embed.add_field(name='Created at', value=created_at, inline=False)
        embed.set_image(url=icon)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the serverinfo command in {interaction.guild.name}")
    
    # Avatar command, get the avatar of a user!

    @app_commands.command(name='avatar', description='Get the avatar of a user!')
    async def avatar(self, interaction: Interaction, user: discord.Member = None):
        if user == None:
            user = interaction.user
        
        embed = discord.Embed(title=f'Avatar for {user}', description=f'Here is the avatar of {user}', color=discord.Color.blue())
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the avatar command in {interaction.guild.name} with the user {user}")
    
    # Invite command, get the invite link for the bot!

    @app_commands.command(name='invite', description='Get the invite link for the bot!')
    async def invite(self, interaction: Interaction):
        embed = discord.Embed(title='Invite', description='Here is the invite link for the bot!', color=discord.Color.blue())
        embed.add_field(name='Invite link', value='__**https://discord.com/api/oauth2/authorize?client_id=1012527409284775977&permissions=8&scope=applications.commands%20bot**__', inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the invite command in {interaction.guild.name}")


    # Rock Papper Scissors command, play rock paper scissors with the bot!

    @app_commands.command(name='rps', description='Play rock paper scissors with the bot!')
    @app_commands.checks.cooldown(1, 5)
    async def rps(self, interaction: Interaction, pchoice: str):
        botchoice = choice(['rock','paper','scissors'])
        if pchoice == botchoice:
            embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nIt\'s a tie!', color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
        elif pchoice == 'rock':
            if botchoice == 'paper':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou lost!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
            elif botchoice == 'scissors':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou won!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
        elif pchoice == 'paper':
            if botchoice == 'rock':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou won!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
            elif botchoice == 'scissors':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou lost!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
        elif pchoice == 'scissors':
            if botchoice == 'rock':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou lost!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
            elif botchoice == 'paper':
                embed = discord.Embed(title=f'You chose {pchoice} and the bot chose {botchoice}! \n\nYou won!', color=discord.Color.blue())
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=f'You have to choose between rock, paper and scissors!', color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
        
        print(f"{interaction.user.name}#{interaction.user.discriminator} used the rps command in {interaction.guild.name} with the choice {pchoice}")


    # Stonks command, get the stonks!

    @app_commands.command(name='stonks', description='Get the stonks!')
    async def stonks(self, interaction: Interaction):

        #Import the list
        from misc.load import stonk_list

        #Get a random stonk
        embed = discord.Embed(title='Stonks', description='Here is your stonk!', color=discord.Color.blue())
        embed.set_image(url=choice(stonk_list))
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the stonks command in {interaction.guild.name}")


    # Roll command, roll a dice!
    @app_commands.command(name='dice', description='Roll a dice!')
    async def roll(self, interaction: Interaction, sides: int = 6, dices: int = 1):
        from random import randint
        # Check if the imputs are both integers
        if not isinstance(dices, int) or not isinstance(sides, int):
            await interaction.response.send_message('Please enter valid numbers!')
        else:
            # Add limits to both dices and sides
            if dices > 10 or sides > 100:
                await interaction.response.send_message('You added too many dices or sides! The limits are 10 dices and 100 sides!')
            else:
                # Roll the dice
                dice = [randint(1, sides) for i in range(dices)]
                dice = ', '.join(map(str, dice))
                embed = discord.Embed(title=f':game_die: Rolling dices! :game_die:', color=discord.Color.blue())
                embed.add_field(name=f'Rolling {dices} dices with {sides} sides each.', value='\u200b', inline=False)
                embed.add_field(name=f'Results: {dice}', value='\u200b', inline=False)
                embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the dice command in {interaction.guild.name} with {dices} dices and {sides} sides")

    # HowGay command - very funny, I know
    @app_commands.command(name='howgay', description='Check how gay you or your friends are!')
    async def howgay(self, interaction: Interaction, member:discord.Member = None):
        if member == None:
            who = interaction.user
        else:
            who = member
        
        from random import randint

        embed = discord.Embed(title='📈 How gay are you 📉', description='\u200b', color=discord.Color.blue())
        embed.add_field(name=f'{who.name} is {randint(0, 100)}% gay!', value='\u200b', inline=False)
        embed.set_thumbnail(url=who.avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the howgay command in {interaction.guild.name} with the member {who.name}#{who.discriminator}")

    # Meme command, get a random meme from reddit
    @app_commands.command(name='meme', description='Get a meme!')
    async def meme(self, interaction: Interaction):
        await interaction.response.send_message('No.')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the meme command in {interaction.guild.name}")

    # Joke command, sends a random joke
    @app_commands.command(name='joke', description='Get a joke!')
    async def joke(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the joke command in {interaction.guild.name}")

    # Quote command, sends a random quote
    @app_commands.command(name='quote', description='Get a quote!')
    async def quote(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the quote command in {interaction.guild.name}")

    # Dad joke, sends a random dad joke
    @app_commands.command(name='dadjoke', description='Get a dad joke!')
    async def dadjoke(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the dadjoke command in {interaction.guild.name}")

    # Cat command, sends a random cat picture
    @app_commands.command(name='cat', description='Get a cat picture!')
    async def cat(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the cat command in {interaction.guild.name}")
    
    # Dog command, sends a random dog picture
    @app_commands.command(name='dog', description='Get a dog picture!')
    async def dog(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the dog command in {interaction.guild.name}")
    
    # Bird command, sends a random bird picture
    @app_commands.command(name='bird', description='Get a bird picture!')
    async def bird(self, interaction: Interaction):
        await interaction.response.send_message('Coming soon!')

        print(f"{interaction.user.name}#{interaction.user.discriminator} used the bird command in {interaction.guild.name}")

    

async def setup(bot:commands.Bot):
    await bot.add_cog(Fun(bot))