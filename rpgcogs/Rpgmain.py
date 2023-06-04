import asyncio
from cProfile import Profile
from multiprocessing import connection
import discord
from discord.ext import commands
from discord import app_commands, Interaction
import asqlite
import random

# Setup the view with the character selection buttons
class CharacterSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='⚔️ Warrior', style=discord.ButtonStyle.blurple)
    async def warrior(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 'Warrior'
        self.stop()
    @discord.ui.button(label='🏹 Archer', style=discord.ButtonStyle.blurple)
    async def archer(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 'Archer'
        self.stop()
    @discord.ui.button(label='🧙‍♂️ Mage', style=discord.ButtonStyle.blurple)
    async def mage(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 'Mage'
        self.stop()
    @discord.ui.button(label='🛡️ Paladin', style=discord.ButtonStyle.blurple)
    async def paladin(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 'Paladin'
        self.stop()
    @discord.ui.button(label='🗡️ Assassin', style=discord.ButtonStyle.blurple)
    async def assassin(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = 'Assassin'
        self.stop()


# View for character deletion
class CharacterDeleteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.red)
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        self.stop()
    @discord.ui.button(label='No', style=discord.ButtonStyle.green)
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        self.stop()


# Setup main cog
class Rpgmain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create a character command
    # ORDER OF DATABASE STATS: 1.id, 2.user_id, 3.name, 4.class, 5.zone, 6.max_zone, 7.level, 8.xp, 9.max_xp, 10.gold, 11.hp, 12.max_hp, 13.attack, 14.defense, 15.agility, 16.luck, 17.intelligence
    @app_commands.command(name='create', description='Start your journey by creating a character')
    @app_commands.checks.cooldown(1, 20)
    async def create(self, interaction: Interaction):

        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Add the buttons
        view = CharacterSelectView()
        await interaction.response.send_message('Choose your class!', view=view)
        await view.wait()
        playerID = interaction.user.id
        playerName = interaction.user.name

        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) == 0:
            if view.value == 'Warrior':
                await cursor.execute(f"""INSERT INTO user_data (user_id, name, class, zone, max_zone, level, xp, xp_cap, gold, hp, max_hp, attack, defense, agility, luck, intelligence) VALUES (
                    {playerID}, '{playerName}', 'Warrior',   1,      1,       1,      0,     50,    0,     40,     40,   7,   5,   5,   5,   5)""")
                    #   ID           NAME         CLASS     ZONE    MZONE   LEVEL      XP    XPCAP   GOLD   HP     MHP   ATK   DEF AGI  LCK INT
                await connection.commit()
                await interaction.edit_original_response(content=f'You have created a {view.value}!')
                print(f'{interaction.user.name} has created a Warrior!')
            elif view.value == 'Archer':
                await cursor.execute(f"""INSERT INTO user_data (user_id, name, class, zone, max_zone, level, xp, xp_cap, gold, hp, max_hp, attack, defense, agility, luck, intelligence) VALUES (
                    {playerID}, '{playerName}', 'Archer', 1, 1, 1, 0, 50, 0, 100, 100, 20, 5, 20, 20, 10)""")
                await connection.commit()
                await interaction.edit_original_response(content=f'You have created an {view.value}!')
                print(f'{interaction.user.name} has created an Archer!')
            elif view.value == 'Mage':
                await cursor.execute(f"""INSERT INTO user_data (user_id, name, class, zone, max_zone, level, xp, xp_cap, gold, hp, max_hp, attack, defense, agility, luck, intelligence) VALUES (
                    {playerID}, '{playerName}', 'Mage', 1, 1, 1, 0, 50, 0, 50, 50, 20, 5, 10, 40, 15)""")
                await connection.commit()
                await interaction.edit_original_response(content=f'You have created a {view.value}!')
                print(f'{interaction.user.name} has created a Mage!')
            elif view.value == 'Paladin':
                await cursor.execute(f"""INSERT INTO user_data (user_id, name, class, zone, max_zone, level, xp, xp_cap, gold, hp, max_hp, attack, defense, agility, luck, intelligence) VALUES (
                    {playerID}, '{playerName}', 'Paladin', 1, 1, 1, 0, 50, 0, 150, 150, 5, 20, 0, 5, 5)""")
                await connection.commit()
                await interaction.edit_original_response(content=f'You have created a {view.value}!')
                print(f'{interaction.user.name} has created a Paladin!')
            elif view.value == 'Assassin':
                await cursor.execute(f"""INSERT INTO user_data (user_id, name, class, zone, max_zone, level, xp, xp_cap, gold, hp, max_hp, attack, defense, agility, luck, intelligence) VALUES (
                    {playerID}, '{playerName}', 'Assassin', 1, 1, 1, 0, 50, 0, 50, 50, 20, 5, 35, 30, 10)""")
                await connection.commit()
                await interaction.edit_original_response(content=f'You have created an {view.value}!')
                print(f'{interaction.user.name} has created an Assassin!')
        else:
            await interaction.edit_original_response(content='You already have a character!')
            print(f'{interaction.user.name} tried to create a character but already has one!')
        
        # Close the connection
        await cursor.close()
        await connection.close()

    # Delete your character command
    @app_commands.command(name='delete', description='Delete your character')
    @app_commands.checks.cooldown(1, 20)
    async def delete(self, interaction: Interaction):

        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()


        # Add the buttons
        view = CharacterDeleteView()
        await interaction.response.send_message('Are you sure you want to delete your character?', view=view)
        await view.wait()

        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) ==0:
            await interaction.response.send_message(content='You don\'t have a character!')
        else:
            if view.value == True:
                await cursor.execute(f"DELETE FROM user_data WHERE user_id = {playerID}")
                await connection.commit()
                await interaction.edit_original_response(content='You have deleted your character!')
            else:
                await interaction.edit_original_response(content='You have not deleted your character!')
    
        # Close the connection
        await cursor.close()
        await connection.close()
    

    # Profile command
    @app_commands.command(name='profile', description='View your profile')
    @app_commands.checks.cooldown(1, 5)
    async def profile(self, interaction: Interaction):
        # Open the database
                connection = await asqlite.connect('database.db')
                cursor = await connection.cursor()
                
                # Get the user's data
                await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (interaction.user.id,))
                user_data = await cursor.fetchone()
                print(user_data) # Debugging
                
                # Check if the user has a profile
                if user_data is None:
                    await interaction.response.edit_message("You don't have a character yet! Use /create to create one!", ephemeral=True)

                # Close the database
                await connection.close()
                
                # Create the embed
                embed = discord.Embed(title=f'{interaction.user.name}\'s Profile', color=discord.Color.blurple())
                embed.set_thumbnail(url=interaction.user.avatar.url)

                # set the profile info values
                profile_value = f"""
                **Class:** {user_data[3]}
                **Level:** {user_data[6]}
                **XP:** {user_data[7]}/{user_data[8]}
                **Health:** {user_data[10]}/{user_data[11]}
                **Gold:** {user_data[9]}
                **Zone:** {user_data[4]}
                **Max Zone:** {user_data[5]}
                """
                # set the stats values
                stats_value = f"""
                **Attack:** {user_data[12]}
                **Defense:** {user_data[13]}
                **Agility:** {user_data[14]}
                **Luck:** {user_data[15]}
                **Intelligence:** {user_data[16]}
                """ 
                embed.add_field(name='__Profile info__', value=profile_value, inline=True)
                embed.add_field(name='__Stats__', value=stats_value, inline=True)
                embed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)



    # Inventory command
    @app_commands.command(name='inventory', description='View your inventory')
    @app_commands.checks.cooldown(1, 5)
    async def inventory(self, interaction: Interaction):
                # Open the database
                connection = await asqlite.connect('database.db')
                cursor = await connection.cursor()
                    
                # Get the user's inventory data
                await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ?", (interaction.user.id,))
                user_inventory = await cursor.fetchall()

                invEmbed = discord.Embed(title=f'{interaction.user.name}\'s Inventory', color=discord.Color.blurple())
                invEmbed.set_thumbnail(url=interaction.user.avatar.url)

                # Format the items by IDs, Names, and Amounts
                item_ids_list = []
                for item in user_inventory:
                    item_ids_list.append(item[1])
                item_ids = '\n'.join(str(item) for item in item_ids_list)
                itemnames_list = []
                for item in user_inventory:
                    itemnames_list.append(item[2])
                itemnames = '\n'.join(str(item) for item in itemnames_list)
                itemamounts_list = []
                for item in user_inventory:
                    itemamounts_list.append(item[3])
                itemamounts = '\n'.join(str(item) for item in itemamounts_list)
                item_sell_price_list = []
                for item in user_inventory:
                    item_sell_price_list.append(item[4])
                item_sell_price = '\n'.join(str(item) for item in item_sell_price_list)

                # Create the embed
                
                invEmbed.add_field(name='__ID__', value=item_ids, inline=True)
                invEmbed.add_field(name='__Name__', value=itemnames, inline=True)
                invEmbed.add_field(name='__Amount__', value=itemamounts, inline=True)
                invEmbed.add_field(name='__Sell Price__', value=item_sell_price, inline=True)
                invEmbed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=invEmbed)
        
        
    # Guide command
    @app_commands.command(name='guide', description='View the guide')
    @app_commands.checks.cooldown(1, 5)
    async def guide(self, interaction: Interaction):
        from misc.load import guide_1
        from misc.load import guide_2


        embed = discord.Embed(title="Guide", description="This is a small guide to help you with the game!", color=discord.Color.green())
        embed.add_field(name="How to get started!", value=guide_1, inline=False)
        embed.add_field(name="Basic commands", value=guide_2, inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    

    # Zone command
    @app_commands.command(name='zone', description='View a specific zone\'s info')
    @app_commands.checks.cooldown(1, 5)
    async def zone(self, interaction: Interaction, zone: int):
        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Retrieve the zone data
        await cursor.execute("SELECT * FROM zone_data WHERE zone_id = ?", (zone,))
        zone_data = await cursor.fetchone()

        # Check if zone exists
        if zone_data is None:
            await interaction.response.send_message(content='That zone doesn\'t exist!')
        else:
            # Create the embed
            embed = discord.Embed(title=f'Zone {zone_data[0]} : {zone_data[1]}', color=discord.Color.blurple())
            if zone_data[0] == 1:
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/769196460600066049/1028333773223362680/unknown.png')
            elif zone_data[0] == 2:
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/769196460600066049/1028333983731290225/unknown.png')
            elif zone_data[0] == 3:
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/769196460600066049/1028334348358926346/unknown.png')
            elif zone_data[0] == 4:
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/769196460600066049/1028335840423858207/unknown.png')
            embed.add_field(name='__Description__', value=f"{zone_data[2]}", inline=False)
            embed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            # Send the embed
            await interaction.response.send_message(embed=embed)
    
    # Travel to zone command
    @app_commands.command(name='travel', description='Travel to a zone')
    @app_commands.checks.cooldown(1, 5)
    async def travel(self, interaction: Interaction, zone: int):
        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Retrieve the zone data
        await cursor.execute("SELECT * FROM zone_data WHERE zone_id = ?", (zone,))
        zone_data = await cursor.fetchone()

        # Check if zone exists
        if zone_data is None:
            await interaction.response.send_message(content='That zone doesn\'t exist!')

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) == 0:
            await interaction.response.send_message(content='You don\'t have a character!')
        
        # Check if the zone is unlocked
        elif zone_data[0] > nonDuplicatedID[0][5]:
            await interaction.response.send_message(content='You haven\'t unlocked that zone yet!')
        
        # Check if the user is already in that zone
        elif zone_data[0] == nonDuplicatedID[0][4]:
            await interaction.response.send_message(content='You are already in that zone!')
        
        # If all the other checks are done, travel to the zone
        else:
            await cursor.execute("UPDATE user_data SET zone = ? WHERE user_id = ?", (zone_data[0], interaction.user.id))
            await connection.commit()
            await interaction.response.send_message(content=f'You have traveled to zone {zone_data[0]}!')

    # List of monsters in a specific zone
    @app_commands.command(name='monsters', description='List of monsters in a specific zone')
    @app_commands.checks.cooldown(1, 5)
    async def monsters(self, interaction: Interaction, zone: int):
        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Retrieve the zone data
        await cursor.execute("SELECT * FROM zone_data WHERE zone_id = ?", (zone,))
        zone_data = await cursor.fetchone()

        # Check if zone exists
        if zone_data is None:
            await interaction.response.send_message(content='That zone doesn\'t exist!')

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) == 0:
            await interaction.response.send_message(content='You don\'t have a character!')
        
        # Check if the zone is unlocked
        elif zone_data[0] > nonDuplicatedID[0][6]:
            await interaction.response.send_message(content='You haven\'t unlocked that zone yet!')
        
        # Give the monster data in the zone
        else:
            await cursor.execute("SELECT * FROM monster_data WHERE zone = ?", (zone_data[0],))
            monster_data = await cursor.fetchall()
            # Create the embed
            embed = discord.Embed(title=f'Monsters in zone {zone_data[0]}', color=discord.Color.blurple())
            for monster in monster_data:
                embed.add_field(name=f'__{monster[1]}__', value=f"Level: {monster[4]}\nHealth: {monster[5]}\nAttack: {monster[7]}\nDefense: {monster[8]}", inline=False)
            embed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
            # Send the embed
            await interaction.response.send_message(embed=embed)

    # The level up command
    @app_commands.command(name='levelup', description='Level up your character')
    @app_commands.checks.cooldown(1, 100)
    async def levelup(self, interaction: Interaction):

        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        print(nonDuplicatedID) # Debugging
        if len(nonDuplicatedID) == 0:
            await interaction.response.send_message(content='You don\'t have a character!')
        
        # Check if the user is able to level up
        if nonDuplicatedID[0][7] < nonDuplicatedID[0][8]:
            await interaction.response.send_message(content='You don\'t have enough experience to level up!')
        
        # Level up the user
        else:
            # Calculate the chance of leveling up
            chance = 100 - (nonDuplicatedID[0][6] * 2.4)
            # Roll the dice
            roll = random.randint(1, 100)
            # Check if the player leveled up
            if roll <= chance:

                # Increase the max xp requirement for the next level
                newXpCap = int(nonDuplicatedID[0][8] * 1.4)
                # Increase the player's level
                newLevel = nonDuplicatedID[0][6] + 1
                # Reset the current xp to 0
                newXp = 0
                # Update the database
                await cursor.execute("UPDATE user_data SET level = ?, xp = ?, xp_cap = ? WHERE user_id = ?", (newLevel, newXp, newXpCap, playerID))
                print (f'{playerID} leveled up to level {newLevel}!') # Debugging
                await connection.commit()
                # Send the message
                embed = discord.Embed(title='Congratulations!', color=discord.Color.blurple())
                embed.add_field(name='You leveled up!', value=f'You are now level {newLevel}!')
                embed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)

            else:
                print (f'{playerID} failed to level up at level {nonDuplicatedID[0][6]}') # Debugging
                embed = discord.Embed(title='Level up failed!', color=discord.Color.red())
                embed.add_field(name='You failed to level up! Sadge :(', value='\u200b', inline=False)
                embed.set_footer(text=f'Interaction requested by {interaction.user.name}', icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)


    # Use heal potions
    @app_commands.command(name='heal', description='Use a heal potion')
    @app_commands.checks.cooldown(1, 5)
    async def heal(self, interaction: Interaction, itemid: str):
        # Connect to database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) == 0:
            await interaction.response.send_message(content='You don\'t have a character! Please create one with /create')
            return
        else:
            # Check if the user has the item
            await cursor.execute(f"SELECT * FROM inventory_data WHERE user_id = {playerID} AND item_id = '{itemid}'")
            item = await cursor.fetchone()
            if item is None:
                await interaction.response.send_message(content='You don\'t have that item!')
                return
            else:
                if item[1] == 1:
                    heal_amount = 25
                elif item[1] == 2:
                    heal_amount = 50
                elif item[1] == 3:
                    heal_amount = 75
                elif item[1] == 4:
                    heal_amount = 100
                else:
                    await interaction.response.send_message(content='That item doesn\'t heal!')
                    return
                # Check if the user is at full health
                if nonDuplicatedID[0][10] == nonDuplicatedID[0][11]:
                    await interaction.response.send_message(content='You are already at full health!')
                    return
                # Check if the user is at max health
                elif nonDuplicatedID[0][10] + heal_amount > nonDuplicatedID[0][11]:
                    await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (nonDuplicatedID[0][11], playerID))
                    await connection.commit()
                    # Check if the user has more than one potion
                    if item[3] > 1:
                        await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_id = ?", (item[3] - 1, playerID, itemid))
                        await connection.commit()
                    else:
                        await cursor.execute(f"DELETE FROM inventory_data WHERE user_id = {playerID} AND item_id = '{itemid}'")
                        await connection.commit()
                    await interaction.response.send_message(content=f'You healed to full health!')
                    return
                # Heal the user
                else:
                    await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (nonDuplicatedID[0][10] + heal_amount, playerID))
                    await connection.commit()
                    # Check if the user has more than one potion
                    if item[3] > 1:
                        await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_id = ?", (item[3] - 1, playerID, itemid))
                        await connection.commit()
                    else:
                        await cursor.execute(f"DELETE FROM inventory_data WHERE user_id = {playerID} AND item_id = '{itemid}'")
                        await connection.commit()
                    embed = discord.Embed(title='Healed!', color=discord.Color.blurple())
                    embed.add_field(name=f'You healed {heal_amount}!\nCurrent health: {nonDuplicatedID[0][10]} / {nonDuplicatedID[0][11]}', value='\u200b', inline=False)
                    return

    # Auto heal
    @app_commands.command(name='heal2', description='/heal is broken, use this instead')
    @app_commands.checks.cooldown(1, 5)
    async def heal2(self, interaction: Interaction):
        # Connect to the database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute(f"SELECT * FROM user_data WHERE user_id = {playerID}")
        nonDuplicatedID = await cursor.fetchall()
        if len(nonDuplicatedID) == 0:
            await interaction.response.send_message(content='You don\'t have a character! Please create one with /create')
            return
        else:
            # Get the user to max health
            await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (nonDuplicatedID[0][11], playerID))
            await connection.commit()
            await interaction.response.send_message(content=f'You healed to full health!')


async def setup(bot:commands.Bot):
    await bot.add_cog(Rpgmain(bot))