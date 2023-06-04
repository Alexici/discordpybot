import discord
from discord.ext import commands
from discord import app_commands
import asqlite
import random


class Rpgeco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # Quick balance check command
    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):

        # Connect to the database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()

        # If the user doesn't have a character
        if playerData is None:
            await interaction.response.send_message("You don't have a character yet! Use /create to make one.", ephemeral=True)
            return
        
        # If the user does have a character
        else:
            embed = discord.Embed(title=f"\U0001fa99 {playerData[2]}'s balance \U0001fa99", color=discord.Color.green())
            embed.add_field(name=f"Gold: {playerData[9]}", value='\u200b', inline=True)
            await interaction.response.send_message(embed=embed)
    
    # Shop command
    @app_commands.command(name="shop", description="Open the shop")
    async def shop(self, interaction: discord.Interaction):
            
            # Connect to the database
            connection = await asqlite.connect('database.db')
            cursor = await connection.cursor()
    
            # Check if the user has a character
            playerID = interaction.user.id
            await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
            playerData = await cursor.fetchone()
    
            # If the user doesn't have a character
            if playerData is None:
                await interaction.response.send_message("You don't have a character yet! Use /create to make one.", ephemeral=True)
                return
            
            # If the user does have a character
            else:
                
                await cursor.execute("SELECT * FROM shop_data")
                shopData = await cursor.fetchall()
                if len (shopData) == 0:
                    await interaction.response.send_message("The shop is empty!", ephemeral=True)
                    return
                else:
                    embed = discord.Embed(title=f"\U0001fa99 Shop \U0001fa99", color=discord.Color.green())
                    # Format the items by IDs, names, price and description
                    item_ids_list = []
                    for item in shopData:
                        item_ids_list.append(item[0])
                    item_ids = '\n'.join(str(item) for item in item_ids_list)
                    item_names_list = []
                    for item in shopData:
                        item_names_list.append(item[1])
                    item_names = '\n'.join(str(item) for item in item_names_list)
                    item_prices_list = []
                    for item in shopData:
                        item_prices_list.append(item[2])
                    item_prices = '\n'.join(str(item) for item in item_prices_list)
                    item_descriptions_list = []
                    for item in shopData:
                        item_descriptions_list.append(item[3])
                    item_descriptions = '\n'.join(str(item) for item in item_descriptions_list)

                    # Add the fields to the embed
                    embed.add_field(name="__ID__", value=item_ids, inline=True)
                    embed.add_field(name="__Name__", value=item_names, inline=True)
                    embed.add_field(name="__Price__", value=item_prices, inline=True)
                    embed.add_field(name="__Description__", value=item_descriptions, inline=True)
                    embed.set_footer(text="Use /buy [item id] to buy an item")
                    await interaction.response.send_message(embed=embed)
    
    # Buy command
    @app_commands.command(name="buy", description="Buy an item from the shop")
    async def buy(self, interaction: discord.Interaction, itemid: str):

        # Connect to the database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()            

        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if len(playerData) == 0:
            await interaction.response.send_message("You don't have a character yet! Use /create to make one.", ephemeral=True)
            return
        else:
            await cursor.execute("SELECT * FROM shop_data WHERE item_id = ?", (itemid,))
            itemData = await cursor.fetchone()
            if len(itemData) == 0:
                await interaction.response.send_message("That item doesn't exist!", ephemeral=True)
                return
            else:
                if playerData[9] < itemData[2]:
                    await interaction.response.send_message("You don't have enough gold!", ephemeral=True)
                    return
                else:
                    await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (playerData[9] - itemData[2], playerID))
                    await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, itemData[0], itemData[1], itemData[3], itemData[2] / 2))
                    await connection.commit()
                    await interaction.response.send_message(f"You bought {itemData[1]} for {itemData[2]} gold!", ephemeral=True)
                    return
     
    
    # Beg command - gives the user a random amount of gold
    @app_commands.command(name="beg", description="Beg for gold lmao")
    @app_commands.checks.cooldown(1, 120)
    async def beg(self, interaction: discord.Interaction):
            
            # Connect to the database
            connection = await asqlite.connect('database.db')
            cursor = await connection.cursor()
    
            # Check if the user has a character
            playerID = interaction.user.id
            await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
            playerData = await cursor.fetchone()
    
            # If the user doesn't have a character
            if playerData is None:
                await interaction.response.send_message("You don't have a character yet! Use /create to make one.", ephemeral=True)
                return
            
            # If the user does have a character
            else:
                from misc.load import beg_no_money, beg_answers
                from random import choice
                chance_to_get_gold = random.randint(1, 100)
                if chance_to_get_gold <= 65:
                    embed = discord.Embed(title=f"\U0001fa99 Begging \U0001fa99", color=discord.Color.green())
                    embed.add_field(name=f"{choice(beg_no_money)} You gained 0 gold.", value='\u200b', inline=True)
                    embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                    await interaction.response.send_message(embed=embed)
                else:
                    gold_gained = random.randint(1, 100)
                    embed = discord.Embed(title=f"\U0001fa99 Begging \U0001fa99", color=discord.Color.green())
                    embed.add_field(name=f"{choice(beg_answers)} You gained {gold_gained} gold.", value='\u200b', inline=True)
                    embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                    await interaction.response.send_message(embed=embed)
                    await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (playerData[9] + gold_gained, playerID))
                    await connection.commit()
    
    # Farm command
    # If no crop is specified, it will show a list with all the crops
    # Crops farmed get added to the user's inventory
    # Sell prices for crops:
    # Wheat: 1 gold
    # Carrot: 2 gold
    # Potato: 4 gold
    # Melon: 6 gold
    # Pumpkin: 8 gold

    @app_commands.command(name="farm", description="Farm crops")
    @app_commands.checks.cooldown(1, 120)
    async def farm(self, interaction: discord.Interaction, crop: str):

        # Connect to the database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        # Check if the user has a character
        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if playerData is None:
            await interaction.response.send_message("You don't have a character yet! Use /create to make one.", ephemeral=True)
            return
        else:
            if crop is None:
                embed = discord.Embed(title=f"\U0001fa99 Farming \U0001fa99", color=discord.Color.green())
                embed.add_field(name=f"Available crops:", value="Wheat, Carrot, Potato, Melon, Pumpkin", inline=True)
                embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                await interaction.response.send_message(embed=embed)
            
            else:

                # Check if the user has the crop's seeds in their inventory
                await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, crop.lower() + " seeds"))
                hasSeed = await cursor.fetchone()
                if hasSeed[2] is not crop:
                    await interaction.response.send_message("You don't have the seeds for that crop!", ephemeral=True)
                    
                else:
                    # Check if the seed type matches the crop type
                    if crop.lower() == "wheat":
                        cropType = "🌾 wheat"
                        cropSellPrice = 1
                        luckgain = playerData[15]
                        maxdrop = 10
                        amount = random.randint(1, maxdrop + luckgain / 2)
                        embed = discord.Embed(title=f"🚜 Farming 🚜", color=discord.Color.green())
                        embed.add_field(name=f"You farmed {amount} {cropType}!", value='\u200b', inline=True)
                        embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                        await interaction.response.send_message(embed=embed)
                        
                        # Check if the user has the crop in their inventory
                        await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, cropType))
                        hasCrop = await cursor.fetchone()
                        if hasCrop is None:
                            await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, 10, cropType, amount, cropSellPrice))
                            await connection.commit()
                        else:
                            await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_name = ?", (hasCrop[3] + amount, playerID, cropType))
                            await connection.commit()

                    
                    elif crop.lower() == "carrot":
                        cropType = "🥕 carrot"
                        cropSellPrice = 3
                        luckgain = playerData[15]
                        maxdrop = 7
                        amount = random.randint(1, maxdrop + luckgain / 2)
                        embed = discord.Embed(title=f"🚜 Farming 🚜", color=discord.Color.green())
                        embed.add_field(name=f"You farmed {amount} {cropType}!", value='\u200b', inline=True)
                        embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                        await interaction.response.send_message(embed=embed)

                        # Check if the user has the crop in their inventory
                        await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, cropType))
                        hasCrop = await cursor.fetchone()
                        if hasCrop is None:
                            await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, 11, cropType, amount, cropSellPrice))
                            await connection.commit()
                        else:
                            await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_name = ?", (hasCrop[3] + amount, playerID, cropType))
                            await connection.commit()
                    
                    elif crop.lower() == "potato":
                        cropType = "🥔 potato"
                        cropSellPrice = 4
                        luckgain = playerData[15]
                        maxdrop = 7
                        amount = random.randint(1, maxdrop + luckgain / 2)
                        embed = discord.Embed(title=f"🚜 Farming 🚜", color=discord.Color.green())
                        embed.add_field(name=f"You farmed {amount} {cropType}!", value='\u200b', inline=True)
                        embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                        await interaction.response.send_message(embed=embed)

                        # Check if the user has the crop in their inventory
                        await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, cropType))
                        hasCrop = await cursor.fetchone()
                        if hasCrop is None:
                            await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, 12, cropType, amount, cropSellPrice))
                            await connection.commit()
                        else:
                            await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_name = ?", (hasCrop[3] + amount, playerID, cropType))
                            await connection.commit()
                        
                    elif crop.lower() == "melon":
                        cropType = "🍈 melon"
                        cropSellPrice = 6
                        luckgain = playerData[15]
                        maxdrop = 5
                        amount = random.randint(1, maxdrop + luckgain / 2)
                        embed = discord.Embed(title=f"🚜 Farming 🚜", color=discord.Color.green())
                        embed.add_field(name=f"You farmed {amount} {cropType}!", value='\u200b', inline=True)
                        embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                        await interaction.response.send_message(embed=embed)

                        # Check if the user has the crop in their inventory
                        await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, cropType))
                        hasCrop = await cursor.fetchone()
                        if hasCrop is None:
                            await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, 13, cropType, amount, cropSellPrice))
                            await connection.commit()
                        else:
                            await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_name = ?", (hasCrop[3] + amount, playerID, cropType))
                            await connection.commit()
                    
                    elif crop.lower() == "pumpkin":
                        cropType = "🎃 pumpkin"
                        cropSellPrice = 12
                        luckgain = playerData[15]
                        maxdrop = 5
                        amount = random.randint(1, maxdrop + luckgain / 2)
                        embed = discord.Embed(title=f"🚜 Farming 🚜", color=discord.Color.green())
                        embed.add_field(name=f"You farmed {amount} {cropType}!", value='\u200b', inline=True)
                        embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}")
                        await interaction.response.send_message(embed=embed)

                        # Check if the user has the crop in their inventory
                        await cursor.execute("SELECT * FROM inventory_data WHERE user_id = ? AND item_name = ?", (playerID, cropType))
                        hasCrop = await cursor.fetchone()
                        if hasCrop is None:
                            await cursor.execute("INSERT INTO inventory_data (user_id, item_id, item_name, item_amount, item_sell_price) VALUES (?, ?, ?, ?, ?)", (playerID, 14, cropType, amount, cropSellPrice))
                            await connection.commit()
                        else:
                            await cursor.execute("UPDATE inventory_data SET item_amount = ? WHERE user_id = ? AND item_name = ?", (hasCrop[3] + amount, playerID, cropType))
                            await connection.commit()


    # Transfer money to another user
    @app_commands.command(name="transfer", description="Transfer money to another user")
    @app_commands.checks.cooldown(1, 50)
    async def transfer(self, interaction: discord.Interaction, amount: int, player: discord.Member):
        # connect to the database
        connection = await asqlite.connect("database.db")
        cursor = await connection.cursor()

        # Get the player's ID
        playerID = interaction.user.id

        # Get the player's data
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if len(playerData) == 0:
            await interaction.response.send_message("You don't have an account yet! Create one with `/create`", ephemeral=True)
            return
        else:
            # Get the other player's data
            player2ID = player.id
            await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (player2ID,))
            player2Data = await cursor.fetchone()
            if len(player2Data) == 0:
                await interaction.response.send_message("That player doesn't have an account yet!", ephemeral=True)
                return
            else:
                # Check if the player has enough money
                if playerData[9] < amount:
                    await interaction.response.send_message("You don't have enough money!", ephemeral=True)
                    return
                else:
                    # Check if the player is trying to transfer to themselves
                    if playerID == player2ID:
                        await interaction.response.send_message("You can't transfer money to yourself!", ephemeral=True)
                        return
                    else:
                        # Transfer the money
                        await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (playerData[9] - amount, playerID))
                        await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (player2Data[9] + amount, player2ID))
                        await connection.commit()
                        await interaction.response.send_message(f"Successfully transferred {amount} coins to {player.mention}!", ephemeral=True)
                        return

async def setup(bot: commands.Bot):
    await bot.add_cog(Rpgeco(bot))