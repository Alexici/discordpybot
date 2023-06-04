import discord
from discord.ext import commands
from discord import app_commands
import asqlite
from random import choice, randint
from misc.load import victory_messages, defeat_messages
import asyncio

class Rpgvs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Fight the monsters of the current zone!
    # Fight details:
    # - You can only fight one monster at a time
    # - You can only fight monsters that are in your current zone
    # - Your health will be reduced after every fight, make sure to heal up!
    # - If you die during a fight, your health will be set to 0 and you wont be able to fight again until you heal up
    # - If you win a fight, you will get gold and XP
    # - At the moment there is no fight cooldown, so the alternative will be 

    # Cooldown the command usage to once every 20 seconds for each user
    @app_commands.command(name="fight", description="Fight the monsters of the current zone!")
    @app_commands.checks.cooldown(1, 30)
    async def fight(self, interaction: discord.Interaction):
        # Connect to the database
        connection = await asqlite.connect('database.db')
        cursor = await connection.cursor()

        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if len(playerData) == 0:
            await interaction.response.send_message("You don't have a character yet! Use /create to create one!", ephemeral=True)
        else:
            print("The data of the player that started the interaction :", playerData)
            await cursor.execute("SELECT * FROM monster_data WHERE zone = ? AND is_boss = ?", (playerData[4], 0))
            monsterData = await cursor.fetchall()
            if len(monsterData) == 0:
                await interaction.response.send_message("There are no monsters in this zone!", ephemeral=True)
            else:

                # Get the monster data
                monster = choice(monsterData)
                monsterHP = monster[5]
                monsterMaxHP = monster[6]
                monsterAttack = monster[7]
                monsterDefense = monster[8]

                # Get the player data
                playerHP = playerData[10]
                playerMaxHP = playerData[11]
                playerAttack = playerData[12]
                playerDefense = playerData[13]
                playerAgility = playerData[14]
                playerLuck = playerData[15]
                playerIntelligence = playerData[16]
                
                playerDodgeChance = playerAgility
                playerCriticalChance = playerLuck * 1.8
                playerCriticalDamage = playerAttack * 2 + playerIntelligence * 1.5

                # Fight main embed
                embed = discord.Embed(title=f"⚔️ Monster fight! ⚔️", description=f"Fight details:", color=0x00ff00)
                embed.add_field(name="Player", value=f"""Name: __**{playerData[2]}**__
                                                    Health: **{playerHP}/{playerMaxHP}**
                                                    Attack: {playerAttack}
                                                    """, inline=True)
                embed.add_field(name="Monster", value=f"""Name: __**{monster[1]}**__
                                                    Health: **{monsterHP}/{monsterMaxHP}**
                                                    Attack: {monsterAttack}
                                                    """, inline=True)
                embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed) # Main embed

                embed.add_field(name="\u200b", value="\u200b", inline=False) #Empty field to add the fight messages

                # Fight loop

                while playerHP > 0 and monsterHP > 0:
                    # Player attack
                    playerAttackRoll = randint(1, 100)
                    if playerAttackRoll <= playerCriticalChance:
                        monsterHP -= int(playerCriticalDamage - (monsterDefense / 100 * playerCriticalDamage))
                        embed.set_field_at(2, name="\u200b", value=f"Critical hit! {playerData[2]} hits monster for {playerCriticalDamage} damage!", inline=False)
                    else:
                        monsterHP -= int(playerAttack - (monsterDefense / 100 * playerAttack))
                        embed.set_field_at(2, name="\u200b", value=f"{playerData[2]} hits monster for {playerAttack} damage!", inline=False)
                    embed.set_field_at(1, name="Monster", value=f"""Name: __**{monster[1]}**__
                                                    Health: **{monsterHP}/{monsterMaxHP}**
                                                    Attack: {monsterAttack}
                                                    """, inline=True)
                    await interaction.edit_original_response(embed=embed)
                    await asyncio.sleep(2)
                    # Check if enemy is dead
                    if monsterHP <= 0:
                        break

                    # Monster attack
                    monsterAttackRoll = randint(1, 100)
                    if monsterAttackRoll <= playerDodgeChance:
                        embed.set_field_at(2, name="\u200b", value=f"The monster missed his attack!", inline=False)
                    else:
                        playerHP -= int(monsterAttack - (playerDefense / 100 * monsterAttack))
                        embed.set_field_at(2, name="\u200b", value=f"{monster[1]} hit the player for {monsterAttack} damage!", inline=False)
                    embed.set_field_at(0, name="Player", value=f"""Name: __**{playerData[2]}**__
                                                    Health: **{playerHP}/{playerMaxHP}**
                                                    Attack: {playerAttack}
                                                    """, inline=True)
                    await interaction.edit_original_response(embed=embed)
                    await asyncio.sleep(2)
                    # Check if player is dead
                    if playerHP <= 0:
                        break

                # Fight end
                if playerHP <= 0:
                    await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (0, playerID))
                    await connection.commit()
                    embed.add_field(name=f"{playerData[2]} lost! {choice(defeat_messages)}", value="\u200b", inline=False)
                    await interaction.edit_original_response(embed=embed)
                elif monsterHP <= 0:
                    await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (playerHP, playerID))
                    await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (playerData[9] + monster[11], playerID))
                    if playerData[7] + monster[10] >= playerData[8]:
                        await cursor.execute("UPDATE user_data SET xp = ? WHERE user_id = ?", (playerData[8], playerID))
                    else:
                        await cursor.execute("UPDATE user_data SET xp = ? WHERE user_id = ?", (playerData[7] + monster[10], playerID))
                    await connection.commit()
                    embed.add_field(name=f"{playerData[2]} won! {choice(victory_messages)}", value="\u200b", inline=False)
                    embed.add_field(name="Rewards", value=f"""Gold: {monster[11]}
                                                            XP: {monster[10]}""")
                    await interaction.edit_original_response(embed=embed)

                    # Check if the player's xp reached the maximum amount
                    if playerData[7] == playerData[8]:
                        embed.add_field(name=f"{playerData[2]} is now able to level up! Please do /levelup when you feel ready!",value="\u200b", inline=False)
                        await interaction.edit_original_response(embed=embed)
                
    
    # Boss Fight command
    # Can only fight the boss of your top zone
    # If you win you cannot fight the boss again
    @app_commands.command(name="bossfight", description="Fight the boss of your top zone!")
    @app_commands.checks.cooldown(1, 100)
    async def bossfight(self, interaction: discord.Interaction):

        connection = await asqlite.connect("database.db")
        cursor = await connection.cursor()

        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if len(playerData) == 0:
            await interaction.response.send_message("You do not have an account! Please make one using /create!", ephemeral=True)
        else:
            if playerData[4] < playerData[5]:
                await interaction.response.send_message("You must be in your top zone in order to fight the boss! Please travel there using /travel.", ephemeral=True)
            else:
                await cursor.execute("SELECT * FROM monster_data WHERE zone = ? AND is_boss = ?", (playerData[5], 1))
                boss = await cursor.fetchone()
                if len(boss) == 0:
                    await interaction.response.send_message("There is no boss in this zone! Please try again later.", ephemeral=True)
                else:
                    # Boss stats
                    bossName = boss[1]
                    bossHp = boss[5]
                    bossMaxHP = boss[6]
                    bossAttack = boss[7]
                    bossDefence = boss[8]
                    bossDodgeChance = boss[9]

                    # Get the player data
                    playerHP = playerData[10]
                    playerMaxHP = playerData[11]
                    playerAttack = playerData[12]
                    playerDefense = playerData[13]
                    playerAgility = playerData[14]
                    playerLuck = playerData[15]
                    playerIntelligence = playerData[16]
                
                    playerDodgeChance = playerAgility
                    playerCriticalChance = playerLuck * 1.8
                    playerCriticalDamage = playerAttack * 2 + playerIntelligence * 1.5

                    # Main Embed
                    embed = discord.Embed(title=f"⚔️ Monster fight! ⚔️", description=f"Fight details:", color=0x00ff00)
                    embed.add_field(name="Player", value=f"""Name: __**{playerData[2]}**__
                                                        Health: **{playerHP}/{playerMaxHP}**
                                                        Attack: {playerAttack}
                                                        """, inline=True)
                    embed.add_field(name="Monster", value=f"""Name: __**{bossName}**__
                                                        Health: **{bossHp}/{bossMaxHP}
                                                        Attack: {bossAttack}
                                                        """, inline=True)
                    embed.add_field(name="\u200b", value="\u200b", inline=False) # Empty field
                    embed.set_footer(text=f"Interaction started by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
                    await interaction.response.send_message(embed=embed)

                    # Fight loop
                    while playerHP > 0 and bossHp > 0:
                        # Player attack
                        playerAttackRoll = randint(1, 100)
                        if playerAttackRoll <= playerCriticalChance:
                            bossHp -= int(playerCriticalDamage - (bossDefence / 100 * playerCriticalDamage))
                            embed.set_field_at(2, name="\u200b", value=f"Critical hit! {playerData[2]} hits monster for {playerCriticalDamage} damage!", inline=False)
                        else:
                            bossHp -= int(playerAttack - (bossDefence / 100 * playerAttack))
                            embed.set_field_at(2, name="\u200b", value=f"{playerData[2]} hits monster for {playerAttack} damage!", inline=False)
                        embed.set_field_at(1, name="Boss", value=f"""Name: __**{boss[1]}**__
                                                            Health: **{bossHp}/{bossMaxHP}**
                                                            Attack: {bossAttack}
                                                            """, inline=True)
                        await interaction.edit_original_response(embed=embed)
                        await asyncio.sleep(2)
                        # check if boss is dead
                        if bossHp <= 0:
                            break


                        # boss attack
                        bossAttackRoll = randint(1, 100)
                        if bossAttackRoll <= playerDodgeChance:
                            embed.set_field_at(2, name="\u200b", value=f"The boss missed his attack!", inline=False)
                        else:
                            playerHP -= int(bossAttack - (playerDefense / 100 * bossAttack))
                            embed.set_field_at(2, name="\u200b", value=f"{boss[1]} hit the player for {bossAttack} damage!", inline=False)
                        embed.set_field_at(0, name="Player", value=f"""Name: __**{playerData[2]}**__
                                                            Health: **{playerHP}/{playerMaxHP}**
                                                            Attack: {playerAttack}
                                                            """, inline=True)
                        await interaction.edit_original_response(embed=embed)
                        await asyncio.sleep(2)
                        # check if player is dead
                        if playerHP <= 0:
                            break

                    # Check if the player won or lost
                    if playerHP <= 0:
                        await cursor.execute("UPDATE user_data SET hp = ? WHERE user_id = ?", (0, playerID))
                        await connection.commit()
                        embed.add_field(name=f"{playerData[2]} lost! {choice(defeat_messages)}", value="\u200b", inline=False)
                        await interaction.edit_original_response(embed=embed)
                    else:
                        await cursor.execute("UPDATE user_data SET hp = ?, max_zone = ? WHERE user_id = ?", (playerMaxHP, playerData[5] + 1, playerID))
                        await cursor.execute("UPDATE user_data SET gold = ? WHERE user_id = ?", (playerData[9] + boss[11], playerID))
                        await connection.commit()
                        embed.add_field(name=f"{playerData[2]} won! {choice(victory_messages)}", value="\u200b", inline=False)
                        embed.add_field(name="You beat the boss and advanced to the next zone! Type /travel to get there!", value="\u200b", inline=False)
                        embed.add_field(name="Rewards", value=f"""Gold: {boss[11]}
                                                                XP: {boss[10]}""", inline=False)      
                        await interaction.edit_original_response(embed=embed)




    # Duel command
    @app_commands.command(name="duel", description="Duel another player!")
    @app_commands.checks.cooldown(1, 120)
    async def duel_command(self, interaction: discord.Interaction, player: discord.Member):
        
        connection = await asqlite.connect("database.db")
        cursor = await connection.cursor()

        playerID = interaction.user.id
        await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (playerID,))
        playerData = await cursor.fetchone()
        if len(playerData) == 0:
            await interaction.response.send_message("You don't have a character yet! Create one with /create")
        else:
            await cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (player.id,))
            enemyData = await cursor.fetchone()
            if len(enemyData) == 0:
                await interaction.response.send_message("That player doesn't have a character yet!")
            else:
                # Get the player data
                playerHP = playerData[10]
                playerMaxHP = playerData[11]
                playerAttack = playerData[12]
                playerDefense = playerData[13]
                playerAgility = playerData[14]
                playerLuck = playerData[15]
                playerIntelligence = playerData[16]
                
                playerDodgeChance = playerAgility
                playerCriticalChance = playerLuck * 1.8
                playerCriticalDamage = playerAttack * 2 + playerIntelligence * 1.5
                
                enemyHP = enemyData[10]
                enemyMaxHP = enemyData[11]
                enemyAttack = enemyData[12]
                enemyDefense = enemyData[13]
                enemyAgility = enemyData[14]
                enemyLuck = enemyData[15]
                enemyIntelligence = enemyData[16]

                enemyDodgeChance = enemyAgility
                enemyCriticalChance = enemyLuck * 1.8
                enemyCriticalDamage = enemyAttack * 2 + enemyIntelligence * 1.5

                embed = discord.Embed(title=f"⚔️ Duel! ⚔️",description="Fight details:", color=0x00ff00)
                embed.add_field(name="Player 1", value=f"""Name: __**{playerData[2]}**__
                                                    HP: **{playerHP} / {playerMaxHP}**
                                                    Attack: {playerAttack}""", inline=True)
                embed.add_field(name="Player 2", value=f"""Name: __**{enemyData[2]}**__
                                                    HP: **{enemyHP} / {enemyMaxHP}**
                                                    Attack: {enemyAttack}""", inline=True)
                embed.set_footer(text=f"Interaction by {interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed) # This is the main message


                embed.add_field(name="\u200b", value="\u200b", inline=False) # Empty field to edit later

                while playerHP > 0 and enemyHP > 0:
                    # Player attack
                    playerAttackHitRoll = randint(1, 100)
                    if playerAttackHitRoll <= enemyDodgeChance:
                        embed.set_field_at(2, name="\u200b", value=f"{playerData[2]} missed his attack!", inline=False)
                    else:
                        playerAttackRoll = randint(1, 100)
                        if playerAttackRoll <= playerCriticalChance:
                            enemyHP -= int(playerCriticalDamage - (enemyDefense / 100 * playerCriticalDamage))
                            embed.set_field_at(2, name="\u200b", value=f"CRITICAL HIT! {playerData[2]} hits {enemyData[2]} for {playerCriticalDamage} damage!", inline=False)
                        else:
                            enemyHP -= int(playerAttack - (enemyDefense / 100 * playerAttack))
                            embed.set_field_at(2, name="\u200b", value=f"{playerData[2]} hits {enemyData[2]} for {playerAttack} damage!", inline=False)
                    embed.set_field_at(1, name="Player 2", value=f"""Name: __**{enemyData[2]}**__
                                                                HP: **{enemyHP} / {enemyMaxHP}**
                                                                Attack: {enemyAttack}""", inline=True) 
                    await interaction.edit_original_response(embed=embed)
                    await asyncio.sleep(2)
                    # check if enemy is dead
                    if enemyHP <= 0:
                        break

                    # Enemy attack
                    enemyAttackHitRoll = randint(1, 100)
                    if enemyAttackHitRoll <= playerDodgeChance:
                        embed.set_field_at(2, name="\u200b", value=f"{enemyData[2]} missed his attack!", inline=False)
                    else:
                        enemyAttackRoll = randint(1, 100)
                        if enemyAttackRoll <= enemyCriticalChance:
                            playerHP -= int(enemyCriticalDamage - (playerDefense / 100 * enemyCriticalDamage))
                            embed.set_field_at(2, name="\u200b", value=f"CRITICAL HIT! {enemyData[2]} hits {playerData[2]} for {enemyCriticalDamage} damage!", inline=False)
                        else:
                            playerHP -= int(enemyAttack - (playerDefense / 100 * enemyAttack))
                            embed.set_field_at(2, name="\u200b", value=f"{enemyData[2]} hits {playerData[2]} for {enemyAttack} damage!", inline=False)
                    embed.set_field_at(0, name="Player 1", value=f"""Name: __**{playerData[2]}**__
                                                                HP: **{playerHP} / {playerMaxHP}**
                                                                Attack: {playerAttack}""", inline=True)
                    await interaction.edit_original_response(embed=embed)
                    await asyncio.sleep(2)
                    # check if player is dead
                    if playerHP <= 0:
                        break
                    

                if playerHP <= 0:
                    embed.add_field(name="\u200b", value=f"__**{enemyData[2]}**__ won the duel! {choice(victory_messages)}", inline=False)
                    await interaction.edit_original_response(embed=embed)
                else:
                    embed.add_field(name="\u200b", value=f"__**{playerData[2]}**__ won the duel! {choice(victory_messages)}", inline=False)
                    await interaction.edit_original_response(embed=embed)
    
async def setup(bot:commands.Bot):
    await bot.add_cog(Rpgvs(bot))